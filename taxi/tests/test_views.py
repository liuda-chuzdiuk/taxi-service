from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")

CARS_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="test",
            password="testpassword"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):

        response = self.client.get(reverse("taxi:driver-list"))
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "test3user123",
            "password2": "test3user123",
            "license_number": "ASS2587415771",
            "first_name": "First name",
            "last_name": "Last name"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_delete_driver(self):
        new_driver = get_user_model().objects.create_user(
            username="test784",
            password="test15874",
            license_number="AHT7841145598"

        )
        self.client.force_login(new_driver)
        self.client.post(reverse("taxi:driver-delete", kwargs={"pk": new_driver.id}))
        self.assertEqual(Driver.objects.count(), 1)


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURERS_URL)

        self.assertEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )

        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="Test1",
            country="Test Country1"
        )
        Manufacturer.objects.create(
            name="Test2",
            country="Test Country2"
        )

        response = self.client.get(MANUFACTURERS_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        form_data = {
            "name": "Test3",
            "country": "Test Country3"
        }

        self.client.post(MANUFACTURER_CREATE_URL, data=form_data)
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])

    def test_update_manufacturer(self):
        new_manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )
        update_data = {
            "name": "Update name",
            "country": "Update country"
        }
        self.client.post(reverse("taxi:manufacturer-update", kwargs={"pk": new_manufacturer.id}), data=update_data)

        manufacturer = Manufacturer.objects.get(pk=new_manufacturer.id)
        self.assertEqual(manufacturer.name, update_data["name"])
        self.assertEqual(manufacturer.country, update_data["country"])

    def test_delete_manufacturer(self):
        new_manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )
        Manufacturer.objects.create(
            name="Delete name",
            country="Delete country"
        )

        self.client.post(reverse("taxi:manufacturer-delete", kwargs={"pk": new_manufacturer.id}))
        self.assertEqual(Manufacturer.objects.count(), 1)


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
