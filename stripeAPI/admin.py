from django.contrib import admin
from .models import Item, Order, Currency, ItemCurrency

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Currency)
admin.site.register(ItemCurrency)
