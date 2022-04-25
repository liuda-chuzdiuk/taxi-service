from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm


class DriverFormTest(TestCase):
    def test_driver_creation_form_with_license_first_last_name_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "test3user123",
            "password2": "test3user123",
            "license_number": "ASS2587415771",
            "first_name": "First name",
            "last_name": "Last name"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class LicenseUpdateTest(TestCase):
    def test_driver_update_form_valid(self):
        new_driver = get_user_model().objects.create_user(
            username="new_user",
            password="test3user123",
            license_number="ASS2587415771",
            first_name="First name",
            last_name="Last name"
        )
        self.client.force_login(new_driver)
        update_data = {
            "license_number": "AAA5874125974"
        }

        self.client.post(reverse("taxi:driver-update", kwargs={"pk": new_driver.id}), data=update_data)

        driver = get_user_model().objects.get(pk=new_driver.id)
        self.assertEqual(driver.license_number, update_data["license_number"])
