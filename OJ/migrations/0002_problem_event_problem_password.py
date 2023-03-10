# Generated by Django 4.1 on 2023-02-09 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CEPHEUS', '0001_initial'),
        ('OJ', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CEPHEUS.event'),
        ),
        migrations.AddField(
            model_name='problem',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]