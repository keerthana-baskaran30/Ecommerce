# Generated by Django 4.0.6 on 2022-08-08 06:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("ecommercepp", "0006_remove_product_sellerid"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="sellerid",
            field=models.CharField(default="null", max_length=10),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="seller",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("phone", models.IntegerField(unique=True)),
                ("sex", models.CharField(max_length=1)),
                ("address", models.CharField(max_length=5000)),
                (
                    "sellerid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]