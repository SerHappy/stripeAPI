from django.shortcuts import redirect, render
import stripe
from django.http import JsonResponse

from stripeAPI.models import Item
from .serializers import ItemSerializer


def home(request):
    items = Item.objects.all()
    ctx = {"items": items}
    return render(request, "home.html", ctx)


def item_info(request, item_id):
    # if request.method == "GET":
    #     return redirect("home")
    item = Item.objects.get(id=item_id)
    ctx = {"item": item}
    return render(request, "item_info.html", ctx)


def buy(request, item_id):
    item = Item.objects.get(id=item_id)

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
    print(data)

    return JsonResponse({"session_id": data["id"]})
