from django.shortcuts import render
from django.shortcuts import get_object_or_404
import stripe
from django.http import HttpResponse, JsonResponse

from stripeAPI.models import Item


def home(request):
    items = Item.objects.all()
    if items is None:
        return HttpResponse("No items found")
    ctx = {"items": items}
    return render(request, "home.html", ctx)


def item_info(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    ctx = {"item": item}
    return render(request, "item_info.html", ctx)


def buy(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

    product = stripe.Product.create(name=item.name)

    price = stripe.Price.create(
        unit_amount=int(item.price) * 100,
        currency="usd",
        product=product,
    )

    data = stripe.checkout.Session.create(
        success_url="http://localhost:8000/",
        line_items=[
            {
                "price": price,
                "quantity": 1,
            },
        ],
        mode="payment",
    )

    return JsonResponse({"session_id": data["id"]})
