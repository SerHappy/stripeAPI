from django.http import JsonResponse
from django.test import Client, TestCase
from django.urls import reverse

from stripeAPI.models import Item


class TestViews(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        Item.objects.create(name="Item 1", description="Description of item 1", price=100)
        Item.objects.create(name="Item 2", description="Description of item 2", price=200)
        Item.objects.create(name="Item 3", description="Description of item 3", price=300)

    def test_home_GET_with_items(self):
        responce = self.client.get(reverse("home"))

        self.assertEqual(responce.status_code, 200)
        self.assertTemplateUsed(responce, "home.html")
        self.assertContains(responce, "Item 1")
        self.assertContains(responce, "Item 2")
        self.assertContains(responce, "Item 3")

    def test_home_GET_without_items(self):
        Item.objects.all().delete()
        responce = self.client.get(reverse("home"))

        self.assertEqual(responce.status_code, 200)
        self.assertTemplateUsed(responce, "home.html")
        self.assertContains(responce, "No items found")

    def test_item_info_GET(self):
        responce = self.client.get(reverse("item", args=[1]))

        self.assertEqual(responce.status_code, 200)
        self.assertTemplateUsed(responce, "item_info.html")

        html = open("templates/test.html").read()

        self.assertHTMLEqual(responce.content.decode(), html)

    def test_item_info_GET_not_existing(self):
        responce = self.client.get(reverse("item", args=[4]))

        self.assertEqual(responce.status_code, 404)

    def test_buy_GET(self):
        responce = self.client.get(reverse("buy", args=[1]))

        self.assertEqual(responce.status_code, 200)
        self.assertIsInstance(responce, JsonResponse)
        self.assertContains(responce, "session_id")

    def test_buy_GET_not_existing(self):
        responce = self.client.get(reverse("buy", args=[4]))

        self.assertEqual(responce.status_code, 404)
