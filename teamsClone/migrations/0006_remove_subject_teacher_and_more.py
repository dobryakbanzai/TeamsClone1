# Generated by Django 4.2.7 on 2023-12-03 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teamsClone', '0005_rename_group_id_users_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='url_online_education',
        ),
        migrations.RemoveField(
            model_name='subjectgroup',
            name='group_id',
        ),
        migrations.RemoveField(
            model_name='subjectgroup',
            name='subject_id',
        ),
        migrations.RemoveField(
            model_name='task',
            name='teacher_id',
        ),
        migrations.AddField(
            model_name='subjectgroup',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teamsClone.group'),
        ),
        migrations.AddField(
            model_name='subjectgroup',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teamsClone.subject'),
        ),
        migrations.AddField(
            model_name='task',
            name='file_byte',
            field=models.BinaryField(null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teamsClone.users'),
        ),
        migrations.AddField(
            model_name='users',
            name='point',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='grouptask',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teamsClone.group'),
        ),
        migrations.AlterField(
            model_name='subjectteacher',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teamsClone.subject'),
        ),
    ]
