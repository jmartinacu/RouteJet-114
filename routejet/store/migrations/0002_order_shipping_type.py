# Generated by Django 4.2.7 on 2023-11-26 17:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="shipping_type",
            field=models.CharField(
                choices=[("NORMAL", "Normal"), ("EXPRESS", "Express")],
                default="NORMAL",
                max_length=7,
            ),
        ),
    ]
