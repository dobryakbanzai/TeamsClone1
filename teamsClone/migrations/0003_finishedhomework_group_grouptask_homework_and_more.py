# Generated by Django 4.2.7 on 2023-12-02 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teamsClone', '0002_rename_user_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinishedHomework',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='GroupTask',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('start_deadline', models.TimeField()),
                ('stop_deadline', models.TimeField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamsClone.group')),
            ],
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('work', models.CharField(max_length=255)),
                ('time_delivery', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='SubjectGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.IntegerField()),
                ('subject_id', models.IntegerField()),
                ('url_online_education', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.DeleteModel(
            name='File',
        ),
        migrations.DeleteModel(
            name='InformationSubject',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='name',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='users',
            old_name='email',
            new_name='password',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='teacher_id',
        ),
        migrations.RemoveField(
            model_name='users',
            name='point',
        ),
        migrations.AddField(
            model_name='subject',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teamsClone.users'),
        ),
        migrations.AddField(
            model_name='subject',
            name='url_online_education',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='file_byte',
            field=models.BinaryField(null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='file_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='telegram_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='subjectteacher',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamsClone.subject'),
        ),
        migrations.AddField(
            model_name='subjectteacher',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamsClone.users'),
        ),
        migrations.AddField(
            model_name='homework',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamsClone.users'),
        ),
        migrations.AddField(
            model_name='grouptask',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamsClone.task'),
        ),
        migrations.AddField(
            model_name='finishedhomework',
            name='homework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamsClone.homework'),
        ),
        migrations.AddField(
            model_name='finishedhomework',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamsClone.task'),
        ),
    ]
