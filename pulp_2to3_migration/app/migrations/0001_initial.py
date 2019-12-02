# Generated by Django 2.2.7 on 2019-12-02 20:44

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0018_auto_20191127_2350'),
    ]

    operations = [
        migrations.CreateModel(
            name='MigrationPlan',
            fields=[
                ('pulp_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pulp_created', models.DateTimeField(auto_now_add=True)),
                ('pulp_last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('plan', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pulp2Content',
            fields=[
                ('pulp_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pulp_created', models.DateTimeField(auto_now_add=True)),
                ('pulp_last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('pulp2_id', models.CharField(max_length=255)),
                ('pulp2_content_type_id', models.CharField(max_length=255)),
                ('pulp2_last_updated', models.PositiveIntegerField()),
                ('pulp2_storage_path', models.TextField(null=True)),
                ('downloaded', models.BooleanField(default=False)),
                ('pulp3_content', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Content')),
            ],
            options={
                'unique_together': {('pulp2_id', 'pulp2_content_type_id')},
            },
        ),
        migrations.CreateModel(
            name='Pulp2Repository',
            fields=[
                ('pulp_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pulp_created', models.DateTimeField(auto_now_add=True)),
                ('pulp_last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('pulp2_object_id', models.CharField(max_length=255, unique=True)),
                ('pulp2_repo_id', models.TextField()),
                ('pulp2_description', models.TextField(null=True)),
                ('pulp2_last_unit_added', models.DateTimeField(null=True)),
                ('pulp2_last_unit_removed', models.DateTimeField(null=True)),
                ('is_migrated', models.BooleanField(default=False)),
                ('type', models.CharField(max_length=25)),
                ('pulp3_repository_version', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.RepositoryVersion')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pulp2LazyCatalog',
            fields=[
                ('pulp_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pulp_created', models.DateTimeField(auto_now_add=True)),
                ('pulp_last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('pulp2_importer_id', models.CharField(max_length=255)),
                ('pulp2_unit_id', models.CharField(max_length=255)),
                ('pulp2_content_type_id', models.CharField(max_length=255)),
                ('pulp2_storage_path', models.TextField()),
                ('pulp2_url', models.TextField()),
                ('pulp2_revision', models.IntegerField(default=0)),
            ],
            options={
                'unique_together': {('pulp2_storage_path', 'pulp2_importer_id', 'pulp2_revision')},
            },
        ),
        migrations.CreateModel(
            name='Pulp2Importer',
            fields=[
                ('pulp_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pulp_created', models.DateTimeField(auto_now_add=True)),
                ('pulp_last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('pulp2_object_id', models.CharField(max_length=255, unique=True)),
                ('pulp2_type_id', models.CharField(max_length=255)),
                ('pulp2_config', django.contrib.postgres.fields.jsonb.JSONField()),
                ('pulp2_last_updated', models.DateTimeField()),
                ('is_migrated', models.BooleanField(default=False)),
                ('pulp2_repository', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pulp_2to3_migration.Pulp2Repository')),
                ('pulp3_remote', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Remote')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pulp2Tag',
            fields=[
                ('pulp_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pulp_created', models.DateTimeField(auto_now_add=True)),
                ('pulp_last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.TextField()),
                ('tagged_manifest', models.CharField(max_length=255)),
                ('repo_id', models.TextField()),
                ('pulp2content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='docker_tag_detail_model', to='pulp_2to3_migration.Pulp2Content')),
            ],
            options={
                'default_related_name': 'docker_tag_detail_model',
                'unique_together': {('name', 'tagged_manifest', 'repo_id', 'pulp2content')},
            },
        ),
        migrations.CreateModel(
            name='Pulp2RepoContent',
            fields=[
                ('pulp_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pulp_created', models.DateTimeField(auto_now_add=True)),
                ('pulp_last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('pulp2_unit_id', models.CharField(max_length=255)),
                ('pulp2_content_type_id', models.CharField(max_length=255)),
                ('pulp2_repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pulp_2to3_migration.Pulp2Repository')),
            ],
            options={
                'unique_together': {('pulp2_repository', 'pulp2_unit_id')},
            },
        ),
        migrations.CreateModel(
            name='Pulp2ManifestList',
            fields=[
                ('pulp_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pulp_created', models.DateTimeField(auto_now_add=True)),
                ('pulp_last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('digest', models.CharField(max_length=255)),
                ('schema_version', models.IntegerField()),
                ('media_type', models.CharField(max_length=80)),
                ('listed_manifests', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), size=None)),
                ('pulp2content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='docker_manifest_list_detail_model', to='pulp_2to3_migration.Pulp2Content')),
            ],
            options={
                'default_related_name': 'docker_manifest_list_detail_model',
                'unique_together': {('digest', 'pulp2content')},
            },
        ),
        migrations.CreateModel(
            name='Pulp2Manifest',
            fields=[
                ('pulp_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pulp_created', models.DateTimeField(auto_now_add=True)),
                ('pulp_last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('digest', models.CharField(max_length=255)),
                ('schema_version', models.IntegerField()),
                ('media_type', models.CharField(max_length=80)),
                ('blobs', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), size=None)),
                ('config_blob', models.CharField(max_length=255, null=True)),
                ('pulp2content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='docker_manifest_detail_model', to='pulp_2to3_migration.Pulp2Content')),
            ],
            options={
                'default_related_name': 'docker_manifest_detail_model',
                'unique_together': {('digest', 'pulp2content')},
            },
        ),
        migrations.CreateModel(
            name='Pulp2ISO',
            fields=[
                ('pulp_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pulp_created', models.DateTimeField(auto_now_add=True)),
                ('pulp_last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.TextField()),
                ('checksum', models.CharField(max_length=64)),
                ('size', models.BigIntegerField()),
                ('pulp2content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='iso_detail_model', to='pulp_2to3_migration.Pulp2Content')),
            ],
            options={
                'default_related_name': 'iso_detail_model',
                'unique_together': {('name', 'checksum', 'size', 'pulp2content')},
            },
        ),
        migrations.CreateModel(
            name='Pulp2Distributor',
            fields=[
                ('pulp_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pulp_created', models.DateTimeField(auto_now_add=True)),
                ('pulp_last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('pulp2_object_id', models.CharField(max_length=255, unique=True)),
                ('pulp2_id', models.TextField()),
                ('pulp2_type_id', models.CharField(max_length=255)),
                ('pulp2_config', django.contrib.postgres.fields.jsonb.JSONField()),
                ('pulp2_auto_publish', models.BooleanField()),
                ('pulp2_last_updated', models.DateTimeField()),
                ('is_migrated', models.BooleanField(default=False)),
                ('pulp2_repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pulp_2to3_migration.Pulp2Repository')),
                ('pulp3_distribution', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.BaseDistribution')),
                ('pulp3_publication', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Publication')),
            ],
            options={
                'unique_together': {('pulp2_repository', 'pulp2_id')},
            },
        ),
        migrations.CreateModel(
            name='Pulp2Blob',
            fields=[
                ('pulp_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pulp_created', models.DateTimeField(auto_now_add=True)),
                ('pulp_last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('digest', models.CharField(max_length=255)),
                ('media_type', models.CharField(max_length=80)),
                ('pulp2content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='docker_blob_detail_model', to='pulp_2to3_migration.Pulp2Content')),
            ],
            options={
                'default_related_name': 'docker_blob_detail_model',
                'unique_together': {('digest', 'pulp2content')},
            },
        ),
    ]
