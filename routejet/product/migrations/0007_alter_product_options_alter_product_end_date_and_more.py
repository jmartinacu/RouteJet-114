# Generated by Django 4.2.7 on 2023-11-25 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_product_end_date_alter_product_num_products_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['country', 'city', 'start_date']},
        ),
        migrations.AlterField(
            model_name='product',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(auto_created=True, max_length=100, unique=True),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['id', 'slug'], name='product_pro_id_b9e5a0_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['country'], name='product_pro_country_1276ec_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['city'], name='product_pro_city_c613d9_idx'),
        ),
    ]