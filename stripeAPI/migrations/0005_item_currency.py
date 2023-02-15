# Generated by Django 4.1.6 on 2023-02-15 18:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stripeAPI", "0004_alter_item_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="currency",
            field=models.CharField(
                choices=[("USD", "usd"), ("EUR", "eur")], default="USD", max_length=3
            ),
        ),
    ]
