# Generated by Django 4.1.6 on 2023-06-26 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_id_code_student_code_rename_id_code_user_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='code',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='code',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
