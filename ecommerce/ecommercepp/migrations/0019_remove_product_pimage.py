# Generated by Django 4.0.6 on 2022-08-08 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "ecommercepp",
            "0018_remove_cart_pid_remove_cart_pname_remove_cart_pprice_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="pimage",
        ),
    ]