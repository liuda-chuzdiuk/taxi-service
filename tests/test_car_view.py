from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CARS_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CARS_URL)

        self.assertEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )

        self.client.force_login(self.user)

    def test_retrieve_car(self):
        new_manufacturer = Manufacturer.objects.create(
            name="Test1",
            country="Test Country1"
        )
        Car.objects.create(
            model="Test Model",
            manufacturer=new_manufacturer
        )

        response = self.client.get(CARS_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_car(self):
        new_manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )
        Car.objects.create(
            model="BMW i4",
            manufacturer=new_manufacturer
        )
        Car.objects.create(
            model="Test",
            manufacturer=new_manufacturer
        )
        Car.objects.create(
            model="Sedan",
            manufacturer=new_manufacturer
        )

        search_param = "I4"
        response = self.client.get(CARS_URL + f"?model={search_param}")
        car = Car.objects.filter(model__icontains=search_param)
        self.assertEqual(
            list(response.context["car_list"]),
            list(car)
        )

    def test_delete_car(self):
        new_manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )
        new_car = Car.objects.create(
            model="Test model",
            manufacturer=new_manufacturer
        )
        Car.objects.create(
            model="Delete model",
            manufacturer=new_manufacturer
        )

        self.client.post(reverse("taxi:car-delete", kwargs={"pk": new_car.id}))
        self.assertEqual(Car.objects.count(), 1)
