# Generated by Django 4.2.7 on 2023-11-25 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_remove_product_product_pro_id_b9e5a0_idx_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='product',
            name='product_pro_id_06b227_idx',
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['id', 'slug'], name='product_pro_id_b9e5a0_idx'),
        ),
    ]