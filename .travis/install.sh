#!/usr/bin/env bash

# WARNING: DO NOT EDIT!
#
# This file was generated by plugin_template, and is managed by bootstrap.py. Please use
# bootstrap.py to update this file.
#
# For more info visit https://github.com/pulp/plugin_template

set -euv

if [ "$TEST" = 'docs' ]; then

  pip install -r ../pulpcore/doc_requirements.txt

  pip install -r doc_requirements.txt
fi

pip install -r functest_requirements.txt

cd $TRAVIS_BUILD_DIR/../pulpcore/containers/

# Although the tag name is not used outside of this script, we might use it
# later. And it is nice to have a friendly identifier for it.
# So we use the branch preferably, but need to replace the "/" with the valid
# character "_" .
#
# Note that there are lots of other valid git branch name special characters
# that are invalid in image tag names. To try to convert them, this would be a
# starting point:
# https://stackoverflow.com/a/50687120
#
# If we are on a tag
if [ -n "$TRAVIS_TAG" ]; then
  TAG=$(echo $TRAVIS_TAG | tr / _)
# If we are on a PR
elif [ -n "$TRAVIS_PULL_REQUEST_BRANCH" ]; then
  TAG=$(echo $TRAVIS_PULL_REQUEST_BRANCH | tr / _)
# For push builds and hopefully cron builds
elif [ -n "$TRAVIS_BRANCH" ]; then
  TAG=$(echo $TRAVIS_BRANCH | tr / _)
  if [ "$TAG" = "master" ]; then
    TAG=latest
  fi
else
  # Fallback
  TAG=$(git rev-parse --abbrev-ref HEAD | tr / _)
fi


PLUGIN=pulp-2to3-migration


# For pulpcore, and any other repo that might check out some plugin PR

if [ -e $TRAVIS_BUILD_DIR/../pulp_file ]; then
  PULP_FILE=./pulp_file
else
  PULP_FILE=git+https://github.com/pulp/pulp_file.git
fi

if [ -e $TRAVIS_BUILD_DIR/../pulp_container ]; then
  PULP_CONTAINER=./pulp_container
else
  PULP_CONTAINER=git+https://github.com/pulp/pulp_container.git
fi
if [ -n "$TRAVIS_TAG" ]; then
  # Install the plugin only and use published PyPI packages for the rest
  cat > vars/vars.yaml << VARSYAML
---
images:
  - ${PLUGIN}-${TAG}:
      image_name: $PLUGIN
      tag: $TAG
      plugins:
        - ./$PLUGIN
        - pulp_file
        - pulp_container
VARSYAML
else
  cat > vars/vars.yaml << VARSYAML
---
images:
  - ${PLUGIN}-${TAG}:
      image_name: $PLUGIN
      tag: $TAG
      pulpcore: ./pulpcore
      plugins:
        - ./$PLUGIN
        - $PULP_FILE
        - $PULP_CONTAINER
VARSYAML
fi
ansible-playbook build.yaml

cd $TRAVIS_BUILD_DIR/../pulp-operator
# Tell pulp-perator to deploy our image
cat > deploy/crds/pulpproject_v1alpha1_pulp_cr.yaml << CRYAML
apiVersion: pulpproject.org/v1alpha1
kind: Pulp
metadata:
  name: example-pulp
spec:
  pulp_file_storage:
    # k3s local-path requires this
    access_mode: "ReadWriteOnce"
    # We have a little over 40GB free on Travis VMs/instances
    size: "40Gi"
  image: $PLUGIN
  tag: $TAG
  database_connection:
    username: pulp
    password: pulp
    admin_password: pulp
CRYAML

# Install k3s, lightweight Kubernetes
.travis/k3s-install.sh
# Deploy pulp-operator, with the pulp containers, according to CRYAML
sudo ./up.sh

# Needed for the script below
# Since it is being run during install rather than actual tests (unlike in
# pulp-operator), and therefore does not trigger the equivalent after_failure
# travis commands.
show_logs_and_return_non_zero() {
    readonly local rc="$?"

    for containerlog in "pulp-api" "pulp-content" "pulp-resource-manager" "pulp-worker"
    do
      echo -en "travis_fold:start:$containerlog"'\\r'
      sudo kubectl logs -l app=$containerlog --tail=10000
      echo -en "travis_fold:end:$containerlog"'\\r'
    done

    return "${rc}"
}
.travis/pulp-operator-check-and-wait.sh || show_logs_and_return_non_zero
