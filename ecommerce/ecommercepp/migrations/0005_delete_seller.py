# Generated by Django 4.0.6 on 2022-08-08 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "ecommercepp",
            "0004_seller_product_sellerid_alter_product_pcategory_and_more",
        ),
    ]

    operations = [
        migrations.DeleteModel(
            name="seller",
        ),
    ]
