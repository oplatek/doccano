# Generated by Django 3.2 on 2021-05-14 06:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0011_merge_0009_tag_0010_auto_20210413_0249'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prob', models.FloatField(default=0.0)),
                ('manual', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta', models.JSONField(default=dict)),
                ('filename', models.FileField(default='.', upload_to='')),
                ('text', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('annotations_approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ImageClassificationProject',
            fields=[
                ('project_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.project')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('api.project',),
        ),
        migrations.CreateModel(
            name='Span',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prob', models.FloatField(default=0.0)),
                ('manual', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_offset', models.IntegerField()),
                ('end_offset', models.IntegerField()),
                ('example', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spans', to='api.example')),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.label')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('example', 'user', 'label', 'start_offset', 'end_offset')},
            },
        ),
        migrations.CreateModel(
            name='TextLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prob', models.FloatField(default=0.0)),
                ('manual', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('example', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='texts', to='api.example')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('example', 'user', 'text')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='documentannotation',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='documentannotation',
            name='document',
        ),
        migrations.RemoveField(
            model_name='documentannotation',
            name='label',
        ),
        migrations.RemoveField(
            model_name='documentannotation',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='seq2seqannotation',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='seq2seqannotation',
            name='document',
        ),
        migrations.RemoveField(
            model_name='seq2seqannotation',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='sequenceannotation',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='sequenceannotation',
            name='document',
        ),
        migrations.RemoveField(
            model_name='sequenceannotation',
            name='label',
        ),
        migrations.RemoveField(
            model_name='sequenceannotation',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='speech2textannotation',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='speech2textannotation',
            name='document',
        ),
        migrations.RemoveField(
            model_name='speech2textannotation',
            name='user',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='randomize_document_order',
            new_name='random_order',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='document',
        ),
        migrations.AlterField(
            model_name='project',
            name='project_type',
            field=models.CharField(choices=[('DocumentClassification', 'document classification'), ('SequenceLabeling', 'sequence labeling'), ('Seq2seq', 'sequence to sequence'), ('Speech2text', 'speech to text'), ('ImageClassification', 'image classification')], max_length=30),
        ),
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.DeleteModel(
            name='DocumentAnnotation',
        ),
        migrations.DeleteModel(
            name='Seq2seqAnnotation',
        ),
        migrations.DeleteModel(
            name='SequenceAnnotation',
        ),
        migrations.DeleteModel(
            name='Speech2textAnnotation',
        ),
        migrations.AddField(
            model_name='example',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examples', to='api.project'),
        ),
        migrations.AddField(
            model_name='category',
            name='example',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='api.example'),
        ),
        migrations.AddField(
            model_name='category',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.label'),
        ),
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='example',
            field=models.ForeignKey(null=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.example'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('example', 'user', 'label')},
        ),
    ]
