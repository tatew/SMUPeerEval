# Generated by Django 3.1.7 on 2021-04-21 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evals', '0009_auto_20210420_2030'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assessmentassigned',
            options={'verbose_name_plural': 'Assessments Assigned'},
        ),
        migrations.AlterModelOptions(
            name='assessmentsubmitted',
            options={'verbose_name_plural': 'Assessments Submitted'},
        ),
        migrations.RemoveField(
            model_name='course',
            name='id',
        ),
        migrations.RemoveField(
            model_name='student',
            name='id',
        ),
        migrations.AddField(
            model_name='course',
            name='CRN',
            field=models.IntegerField(default=-1, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='student',
            name='studentNumber',
            field=models.IntegerField(default=-1, primary_key=True, serialize=False),
        ),
    ]
