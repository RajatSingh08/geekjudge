# Generated by Django 4.0 on 2022-07-10 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OJ', '0002_problem_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='name',
        ),
    ]