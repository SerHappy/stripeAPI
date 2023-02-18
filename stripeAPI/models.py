from django.db import models


class Order(models.Model):
    order_number = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number


class Currency(models.Model):
    CURRENCIES = (("USD", "usd"), ("EUR", "eur"))
    currency = models.CharField(max_length=3, choices=CURRENCIES, default="usd")

    def __str__(self) -> str:
        return self.currency


class Item(models.Model):
    name = models.CharField(max_length=100)
    order = models.ForeignKey(
        "Order", on_delete=models.SET_NULL, blank=True, null=True
    )
    quantity = models.IntegerField(default=1)
    description = models.TextField()

    def __str__(self):
        return self.name


class ItemCurrency(models.Model):
    item = models.ForeignKey(
        "Item", on_delete=models.CASCADE, blank=True, null=True
    )
    currency = models.ForeignKey(
        "Currency", on_delete=models.CASCADE, blank=True, null=True
    )
    price = models.FloatField()

    def __str__(self) -> str:
        return f"{self.price}"
