from django.http import JsonResponse
from django.test import Client, TestCase
from django.urls import reverse

from stripeAPI.models import Currency, Item, ItemCurrency, Order


class TestViews(TestCase):
    """This class contains all the tests for the views.

    Args:
        TestCase (TestCase): TestCase class from django
    """

    def setUp(self) -> None:
        """This method is called before each test."""

        self.client = Client()
        item1 = Item.objects.create(
            name="Item 1", description="Description of item 1"
        )
        item2 = Item.objects.create(
            name="Item 2", description="Description of item 2"
        )
        item3 = Item.objects.create(
            name="Item 3", description="Description of item 3"
        )

        currency1 = Currency.objects.create(currency="USD")
        currency2 = Currency.objects.create(currency="EUR")

        ItemCurrency1 = ItemCurrency.objects.create(
            item=item1, currency=currency1, price=100
        )
        ItemCurrency2 = ItemCurrency.objects.create(
            item=item1, currency=currency2, price=94
        )

        ItemCurrency3 = ItemCurrency.objects.create(
            item=item2, currency=currency1, price=200
        )
        ItemCurrency4 = ItemCurrency.objects.create(
            item=item2, currency=currency2, price=187
        )

        ItemCurrency5 = ItemCurrency.objects.create(
            item=item3, currency=currency1, price=300
        )
        ItemCurrency6 = ItemCurrency.objects.create(
            item=item3, currency=currency2, price=280
        )

        order = Order.objects.create(order_number=1234567890)

    def test_home_GET_with_items(self) -> None:
        """This method tests the home view with items in the database."""

        responce = self.client.get(reverse("home"))

        self.assertEqual(responce.status_code, 200)
        self.assertTemplateUsed(responce, "home.html")
        self.assertContains(responce, "Item 1")
        self.assertContains(responce, "Item 2")
        self.assertContains(responce, "Item 3")

    def test_home_GET_without_items(self) -> None:
        """This method tests the home view without items in the database."""

        Item.objects.all().delete()
        responce = self.client.get(reverse("home"))

        self.assertEqual(responce.status_code, 200)
        self.assertTemplateUsed(responce, "home.html")
        self.assertContains(responce, "No items found")

    def test_home_GET_with_order(self) -> None:
        """This method tests the home view with order in the database."""

        responce = self.client.get(reverse("home"))

        session_id = responce.cookies.copy()["sessionid"].value

        order = Order.objects.create(order_number=session_id)
        order.save()

        item1 = Item.objects.get(id=1)
        item1.order = order
        item1.save()

        responce = self.client.get(reverse("home"))

        self.assertEqual(responce.status_code, 200)
        self.assertTemplateUsed(responce, "home.html")
        self.assertContains(responce, "Your Order:")

    def test_home_GET_without_currency(self) -> None:
        """This method tests the home view without currency in the database."""

        Currency.objects.all().delete()
        responce = self.client.get(reverse("home"))

        self.assertEqual(responce.status_code, 404)

    def test_item_info_GET(self) -> None:
        """This method tests the item_info view with an item in the database."""

        responce = self.client.get(reverse("item", args=[1]))

        self.assertEqual(responce.status_code, 200)
        self.assertTemplateUsed(responce, "item_info.html")

    def test_item_info_GET_not_existing(self) -> None:
        """This method tests the item_info view with an item that does not exist in the database."""

        responce = self.client.get(reverse("item", args=[4]))

        self.assertEqual(responce.status_code, 404)

    def test_add_GET_with_order(self) -> None:
        """This method tests the add view with an order in the database."""

        responce = self.client.get(reverse("add", args=[1]))

        self.assertEqual(responce.status_code, 302)

    def test_add_GET_without_order(self) -> None:
        """This method tests the add view with an empty order in the database."""

        responce = self.client.get(reverse("add", args=[1]))

        self.assertEqual(responce.status_code, 302)

    def test_add_GET_not_existing(self) -> None:
        """This method tests the add view with an order  that does not exist in the database."""

        responce = self.client.get(reverse("add", args=[4]))

        self.assertEqual(responce.status_code, 404)

    def test_buy_GET(self) -> None:
        """This method tests the buy view with an item in the database."""

        responce = self.client.get(reverse("buy", args=[1]))

        self.assertEqual(responce.status_code, 200)
        self.assertIsInstance(responce, JsonResponse)
        self.assertContains(responce, "session_id")

    def test_buy_GET_with_currency(self) -> None:
        """This method tests the buy view with an item in the database."""

        responce = self.client.get("%s?currency=USD" % reverse("buy", args=[1]))

        self.assertEqual(responce.status_code, 200)
        self.assertIsInstance(responce, JsonResponse)
        self.assertContains(responce, "session_id")

    def test_buy_GET_with_not_exists_currency(self) -> None:
        """This method tests the buy view with an item in the database."""

        responce = self.client.get("%s?currency=RUB" % reverse("buy", args=[1]))

        self.assertEqual(responce.status_code, 200)
        self.assertIsInstance(responce, JsonResponse)
        self.assertContains(responce, "session_id")

    def test_buy_GET_not_existing(self) -> None:
        """This method tests the buy view with an item that does not exist in the database."""

        responce = self.client.get(reverse("buy", args=[4]))

        self.assertEqual(responce.status_code, 404)

    def test_order_GET(self) -> None:
        """This method tests the order view with an order in the database."""

        responce = self.client.get(reverse("home"))

        session_id = responce.cookies.copy()["sessionid"].value

        order = Order.objects.create(order_number=session_id)
        order.save()

        item1 = Item.objects.get(id=1)
        item1.order = order
        item1.save()

        responce = self.client.get(reverse("order", args=[2]))

        self.assertEqual(responce.status_code, 200)
        self.assertIsInstance(responce, JsonResponse)
        self.assertContains(responce, "session_id")

    def test_order_GET_not_exists(self) -> None:
        """This method tests the order view with an order that does not exist in the database."""

        responce = self.client.get(reverse("order", args=[4]))

        self.assertEqual(responce.status_code, 404)

    def test_order_GET_without_items(self) -> None:
        """This method tests the order view with an empty order in the database."""

        responce = self.client.get(reverse("order", args=[1]))

        self.assertEqual(responce.status_code, 404)
