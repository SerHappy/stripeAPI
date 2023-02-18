from django.shortcuts import redirect, render, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse, Http404
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
    try:
        items = (
            ItemCurrency.objects.prefetch_related("item")
            .filter(currency=Currency.objects.get(currency="USD"))
            .values("item__id", "item__name", "item__description", "price")
        )
    except (Currency.DoesNotExist):
        raise Http404

    if items is None:
        return render(request, "home.html")

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
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            raise Http404
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

        currency_usd = Currency.objects.get(currency="USD")
        currency_eur = Currency.objects.get(currency="EUR")

        item_usd_price = (
            int(
                ItemCurrency.objects.get(
                    item=item_id, currency=currency_usd
                ).price
            )
            * 100
        )
        item_eur_price = (
            int(
                ItemCurrency.objects.get(
                    item=item_id, currency=currency_eur
                ).price
            )
            * 100
        )

        price = stripe.Price.create(
            expand=["currency_options"],
            unit_amount=item_usd_price,
            currency="usd",
            currency_options={
                "eur": {
                    "unit_amount": item_eur_price,
                },
            },
            product=product,
        )
        if request.GET.get("currency") is None:
            session_currency = "usd"
        else:
            if Currency.objects.filter(
                currency=request.GET["currency"]
            ).exists():
                session_currency = request.GET["currency"]
            else:
                session_currency = "usd"

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
            currency=session_currency,
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
        order = get_object_or_404(
            Order, id=order_id, order_number=_order_id(request)
        )
        items = Item.objects.filter(order=order)

        if items.count() == 0:
            raise Http404

        stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

        line_items = []

        for item in items:
            currency_usd = Currency.objects.get(currency="USD")
            item_usd_price = (
                int(
                    ItemCurrency.objects.get(
                        item=item.id, currency=currency_usd
                    ).price
                )
                * 100
            )

            line_items.append(
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": item.name,
                        },
                        "unit_amount": item_usd_price,
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
