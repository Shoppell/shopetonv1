# Generated by Django 4.0.2 on 2022-03-14 23:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_product_sale_availble'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='sale_availble',
            new_name='sale_available',
        ),
    ]