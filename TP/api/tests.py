import pytest
from rest_framework.test import APIClient
from api.serializers import *


class TestCreate:
    @pytest.mark.django_db
    @pytest.mark.parametrize(
        ['user_id', 'item_id', "expected"],
        [
            (1, 1, 201),
            (100, 100, 400),
        ]
    )
    def test_inventory_create(self, user_id, item_id, expected):
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
            currency=Currency.objects.get(name='name'),
            details="test",

        )
        api_client = APIClient()
        api_client.force_authenticate(user=User.objects.get(username='username'))
        url = 'http://127.0.0.1:8000/api/inventory/'
        data = {
            "id": 1,
            "user": user_id,
            "item": item_id,
            "quantity": 1,
        }

        response = api_client.post(url, data)
        assert response.status_code == expected

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        ['quantity', "expected"],
        [
            (1, 201),
            (100, 400),
        ]
    )
    def test_offer_create(self, quantity, expected):
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
            currency=Currency.objects.get(name='name'),
            details="test",

        )
        Inventory.objects.create(
            user=User.objects.get(username='username'),
            item=Item.objects.get(name='name'),
            quantity=10
        )
        url = 'http://127.0.0.1:8000/api/offer/'
        inventory = Inventory.objects.get(user=User.objects.get(username='username'))
        api_client = APIClient()
        api_client.force_authenticate(user=User.objects.get(username='username'))
        data = {
            "user": User.objects.get(username="username").id,
            "item": Item.objects.get(name="name").id,
            "entry_quantity": quantity,
            "quantity": 1,
            "offer_type": 2,
            "price": 1
        }
        response = api_client.post(url, data)
        assert response.status_code == expected


class TestApi:
    @pytest.fixture()
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
            price="1.11",
            currency=Currency.objects.get(),
            details="test",
        )

        WatchList.objects.create(user=User.objects.get(), item=Item.objects.get())

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
        response = self.client.get("http://127.0.0.1:8000/api/currency/")
        assert response.status_code == 200
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_get_item(self, setUp):
        response = self.client.get("http://127.0.0.1:8000/api/item/")
        assert response.status_code == 200
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_get_watchlist(self, setUp):
        response = self.client.get("http://127.0.0.1:8000/api/watch-list/")
        assert response.status_code == 200
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_get_offer(self, setUp):
        response = self.client.get("http://127.0.0.1:8000/api/offer/")
        assert response.status_code == 200
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_get_inventory(self, setUp):
        response = self.client.get("http://127.0.0.1:8000/api/inventory/")
        assert response.status_code == 200
        assert len(response.data) == 1
