# Generated by Django 4.0 on 2022-07-12 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OJ', '0015_alter_submission_verdict'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='solved_status',
            field=models.CharField(choices=[('Unsolved', 'Unsolved'), ('Solved', 'Solved')], default='Unsolved', max_length=10),
        ),
    ]