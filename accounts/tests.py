from django.test import TestCase
from rest_framework.exceptions import ErrorDetail

from accounts.serializers import RegistrationSerializer


class RegistrationSerializerTest(TestCase):
    def setUp(self):
        data_valid = {
            'username': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@mail.com',
            'password': '12',
            'confirm_password': '12'
        }

        self.serializer = RegistrationSerializer(data=data_valid)

        self.invalid_data = {
            'username': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'email': 'salom@gmail.com',
            'password': '12',
            'confirm_password': '123'
        }
        self.invalid_serializer = RegistrationSerializer(data=self.invalid_data)

    def test_registration_valid(self):
        self.assertTrue(self.serializer.is_valid())

    def test_registration_invalid(self):
        self.assertFalse(self.invalid_serializer.is_valid())
        self.assertEqual(self.invalid_serializer.errors, {
            'non_field_errors': [ErrorDetail(string='password and confirm_password are not equal', code='invalid')]}
                         )

    def test_create_user(self):
        self.serializer.is_valid()
        user = self.serializer.save()
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.first_name, 'test')
