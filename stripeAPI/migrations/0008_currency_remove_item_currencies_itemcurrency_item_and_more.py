# Generated by Django 4.1.6 on 2023-02-15 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("stripeAPI", "0007_itemcurrency_remove_item_currency_item_currencies"),
    ]

    operations = [
        migrations.CreateModel(
            name="Currency",
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
                (
                    "currency",
                    models.CharField(
                        choices=[("USD", "usd"), ("EUR", "eur")],
                        default="usd",
                        max_length=3,
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="item",
            name="currencies",
        ),
        migrations.AddField(
            model_name="itemcurrency",
            name="item",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="stripeAPI.item",
            ),
        ),
        migrations.AlterField(
            model_name="itemcurrency",
            name="currency",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="stripeAPI.currency",
            ),
        ),
    ]
