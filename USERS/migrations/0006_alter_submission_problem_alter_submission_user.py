# Generated by Django 4.1 on 2022-09-09 16:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OJ', '0001_initial'),
        ('USERS', '0005_alter_submission_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='problem',
            field=models.ForeignKey(null=True, on_delete=models.SET('deleted'), to='OJ.problem'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='user',
            field=models.ForeignKey(null=True, on_delete=models.SET('deleted'), to=settings.AUTH_USER_MODEL),
        ),
    ]