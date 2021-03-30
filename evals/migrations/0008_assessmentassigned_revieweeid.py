# Generated by Django 3.1.7 on 2021-03-30 02:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evals', '0007_remove_assessmentassigned_revieweeid'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessmentassigned',
            name='revieweeID',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.RESTRICT, related_name='AssessmentGrade', to='evals.student'),
            preserve_default=False,
        ),
    ]
