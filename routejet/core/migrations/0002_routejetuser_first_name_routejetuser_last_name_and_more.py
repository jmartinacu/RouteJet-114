# Generated by Django 4.2.7 on 2023-12-06 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='routejetuser',
            name='first_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='routejetuser',
            name='last_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='routejetuser',
            name='postal_code',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
