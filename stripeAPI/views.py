from django.shortcuts import redirect, render, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from stripeAPI.models import Currency, Item, ItemCurrency, Order

import stripe


def _order_id(request):
    """This function will create a order id for the user if the user does not have one.

    Args:
        request (WSGIRequest): request object

    Returns:
        int: order id
    """

    order_id = request.session.session_key
    if not order_id:
        order_id = request.session.create()
    return order_id


def home(request: WSGIRequest) -> HttpResponse:
    """This is the view that will be called when the user visits the home page.

    Args:
        request (WSGIRequest): request object

    Returns:
        HttpResponse: a Http response with the home page
    """

    items = (
        ItemCurrency.objects.prefetch_related("item")
        .filter(currency=Currency.objects.get(currency="USD"))
        .values("item__id", "item__name", "item__description", "price")
    )

    if items is None:
        return HttpResponse("No items found")

    ctx = {"items": items}

    try:
        order = Order.objects.get(order_number=_order_id(request))
        order_items = Item.objects.filter(order=order.id)
        ctx = {"items": items, "order": order, "order_items": order_items}
    except Order.DoesNotExist:
        pass

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
    item_prices = ItemCurrency.objects.filter(item=item_id)
    ctx = {"item": item, "item_prices": item_prices}
    return render(request, "item_info.html", ctx)


def add_to_cart(request: WSGIRequest, item_id: int) -> HttpResponse:
    """This is the view that will be called when the user clicks on the add to cart button.

    Args:
        request (WSGIRequest): request object
        item_id (int): id of the item that the user wants to buy

    Returns:
        HttpResponse: a Http response with the item info
    """
    try:
        order = Order.objects.get(order_number=_order_id(request))
    except Order.DoesNotExist:
        order = Order.objects.create(order_number=_order_id(request))
        order.save()

    try:
        item = Item.objects.get(id=item_id, order=order)
        item.quantity += 1
    except Item.DoesNotExist:
        item = Item.objects.get(id=item_id)
        item.order = order
        item.quantity = 1
    item.save()

    return redirect("home")


class BuyAPIView(APIView):
    """This is the view that will be called when the user clicks on the buy button.

    Args:
        APIView (APIView): Base class for all API views.

    """

    def get(self, request: WSGIRequest, item_id: int) -> JsonResponse:
        """This method is called when GET request is sent to the server.

        Args:
            request (WSGIRequest): request object
            item_id (int): id of the item that the user wants to buy

        Returns:
            JsonResponse: a json response with the session id
        """
        item = get_object_or_404(Item, id=item_id)

        stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

        product = stripe.Product.create(name=item.name)

        item_currency_usd = Currency.objects.get(currency="USD")
        item_currency_eur = Currency.objects.get(currency="EUR")

        price = stripe.Price.create(
            expand=["currency_options"],
            unit_amount=int(ItemCurrency.objects.get(item=item_id, currency=item_currency_usd).price) * 100,
            currency="usd",
            currency_options={
                "eur": {
                    "unit_amount": int(ItemCurrency.objects.get(item=item_id, currency=item_currency_eur).price) * 100,
                },
            },
            product=product,
        )

        session = stripe.checkout.Session.create(
            success_url="http://localhost:8000/",
            cancel_url="http://localhost:8000/",
            line_items=[
                {
                    "price": price,
                    "quantity": 1,
                },
            ],
            mode="payment",
            currency=request.GET["currency"],
            payment_method_types=["card"],
        )

        return JsonResponse({"session_id": session["id"]})


class OrderBuyAPIView(APIView):
    """This is the view that will be called when the user clicks on the OrderBuy button.

    Args:
        APIView (APIView): Base class for all API views.

    """

    def get(self, request: WSGIRequest, order_id: int) -> JsonResponse:
        """This method is called when GET request is sent to the server.

        Args:
            request (WSGIRequest): request object
            order_id (int): id of the order that the user wants to buy

        Returns:
            JsonResponse: a json response with the session id
        """
        order = Order.objects.get(id=order_id, order_number=_order_id(request))
        items = Item.objects.filter(order=order)

        stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

        line_items = []

        for item in items:
            item_currency_usd = Currency.objects.get(currency="USD")

            line_items.append(
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": item.name,
                        },
                        "unit_amount": int(ItemCurrency.objects.get(item=item.id, currency=item_currency_usd).price)
                        * 100,
                    },
                    "quantity": item.quantity,
                }
            )

        session = stripe.checkout.Session.create(
            success_url="http://localhost:8000/",
            cancel_url="http://localhost:8000/",
            line_items=line_items,
            mode="payment",
            payment_method_types=["card"],
        )

        return JsonResponse({"session_id": session["id"]})
