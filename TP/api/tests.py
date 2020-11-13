import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from app.models import Offer, Currency, Inventory, Item, WatchList, Price


class TestApi:
    @pytest.fixture()
    @pytest.mark.django_db
    def setUp(self):
        User.objects.create(
            username="username",
            email="user@gmail.com",
            password="user_password",
            first_name="user",
            last_name="user_user",
        )

        Currency.objects.create(code="code", name="name")

        Item.objects.create(
            code="code",
            name="name",
            price="1.11",
            currency=Currency.objects.get(),
            details="test",

        )

        WatchList.objects.create(user=User.objects.get(), item=Item.objects.get())

        Price.objects.create(
            currency=Currency.objects.get(),
            item=Item.objects.get(),
            price="1.11",
        )

        Offer.objects.create(
            user=User.objects.get(),
            item=Item.objects.get(),
            entry_quantity=1,
            quantity=1,
            order_type=1,
            price="1.11",
        )

        Inventory.objects.create(
            user=User.objects.get(),
            item=Item.objects.get(),
            quantity=1,
        )

        self.client = APIClient()
        self.client.login()

    @pytest.mark.django_db
    def test_get_currency(self, setUp):
        response = self.client.get("/api/currency/")
        assert response.status_code == 200
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_get_item(self, setUp):
        response = self.client.get("/api/item/")
        assert response.status_code == 200
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_get_watchlist(self, setUp):
        response = self.client.get("/api/watch-list/")
        assert response.status_code == 200
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_get_offer(self, setUp):
        response = self.client.get("/api/offer/")
        assert response.status_code == 200
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_get_inventory(self, setUp):
        response = self.client.get("/api/inventory/")
        assert response.status_code == 200
        assert len(response.data) == 1
