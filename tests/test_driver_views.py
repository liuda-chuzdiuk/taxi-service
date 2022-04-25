from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver


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
