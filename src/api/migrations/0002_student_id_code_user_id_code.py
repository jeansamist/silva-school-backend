# Generated by Django 4.1.6 on 2023-06-26 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='id_code',
            field=models.CharField(blank=True, max_length=8, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='id_code',
            field=models.CharField(blank=True, max_length=8, null=True, unique=True),
        ),
    ]
