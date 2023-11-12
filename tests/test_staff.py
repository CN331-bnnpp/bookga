from django.test import TestCase
from django.urls import reverse, resolve
from django.urls.conf import include
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class TestUrls(TestCase):
    def test_about_url_resolves(self):
        url = reverse('about')
        self.assertEqual(url, '/about')
        resolver = resolve(url)
        self.assertEqual(resolver.url_name, 'about')

    def test_about_included_url_resolves(self):
        included_url = reverse('about') 
        self.assertEqual(included_url, '/about')  
        resolver = resolve(included_url)
        self.assertEqual(resolver.url_name, 'about')  


class TestView(TestCase):
    def setUp(self):
        # Create a user for testing
        self.staff_user = User.objects.create_user(username='staffuser', password='testpassword', is_staff=True)
        self.regular_user = User.objects.create_user(username='regularuser', password='testpassword')

    def test_staff_view_authenticated_staff_user(self):
        self.client.login(username='staffuser', password='testpassword')
        response = self.client.get(reverse('gate'))

        self.assertEqual(response.status_code, 200)

    def test_staff_view_authenticated_regular_user(self):
        # Log in the regular user using the test client
        self.client.login(username='regularuser', password='testpassword')
        response = self.client.get(reverse('gate'))
