# Generated by Django 4.0.6 on 2022-08-08 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ecommercepp", "0011_rename_sellername_seller_sellerid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="sellerid",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="ecommercepp.seller"
            ),
        ),
    ]
