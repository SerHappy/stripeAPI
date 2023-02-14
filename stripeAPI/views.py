from django.shortcuts import render, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse

from stripeAPI.models import Item

import stripe


def home(request: WSGIRequest) -> HttpResponse:
    """This is the view that will be called when the user visits the home page.

    Args:
        request (WSGIRequest): request object

    Returns:
        HttpResponse: a Http response with the home page
    """

    items = Item.objects.all()
    if items is None:
        return HttpResponse("No items found")
    ctx = {"items": items}
    return render(request, "home.html", ctx)


def item_info(request: WSGIRequest, item_id: int) -> HttpResponse:
    """This is the view that will be called when the user clicks on an item.

    Args:
        request (WSGIRequest): request object
        item_id (int): id of the item that the user wants to buy

    Returns:
        HttpResponse: a Http response with the item info
    """

    item = get_object_or_404(Item, id=item_id)
    ctx = {"item": item}
    return render(request, "item_info.html", ctx)


def buy(request: WSGIRequest, item_id: int) -> JsonResponse:
    """This is the view that will be called when the user clicks the buy button.

    Args:
        request (WSGIRequest): request object
        item_id (int): id of the item that the user wants to buy

    Returns:
        JsonResponse: a json response with the session id
    """

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
