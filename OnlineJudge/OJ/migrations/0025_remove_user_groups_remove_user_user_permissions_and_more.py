# Generated by Django 4.0 on 2022-07-22 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OJ', '0024_alter_submission_options_remove_submission_user_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.AlterModelOptions(
            name='submission',
            options={},
        ),
        migrations.RemoveField(
            model_name='problem',
            name='description_new',
        ),
        migrations.RemoveField(
            model_name='problem',
            name='memory_limit',
        ),
        migrations.RemoveField(
            model_name='problem',
            name='time_limit',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='language',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='user',
        ),
        migrations.AddField(
            model_name='submission',
            name='user_code',
            field=models.TextField(default='', max_length=100000),
        ),
        migrations.AlterField(
            model_name='problem',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='submission',
            name='verdict',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.DeleteModel(
            name='Code',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
