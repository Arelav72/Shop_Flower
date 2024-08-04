from django.test import TestCase
# shop/tests/test_views.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from users.forms import UserCreationForm

class RegisterViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertIsInstance(response.context['form'], UserCreationForm)

    def test_register_view_post_valid(self):
        form_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(reverse('register'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect to main
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_view_post_invalid(self):
        form_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'differentpassword',  # Passwords do not match
        }
        response = self.client.post(reverse('register'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertFalse(User.objects.filter(username='testuser').exists())
        self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')

# Create your tests here.
