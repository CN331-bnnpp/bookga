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
        # self.assertEqual(resolver.app_name, 'about')

    def test_about_included_url_resolves(self):
        included_url = reverse('about') 
        self.assertEqual(included_url, '/about')  
        resolver = resolve(included_url)
        self.assertEqual(resolver.url_name, 'about')  


class TestView(TestCase):
    def setUp(self):
        # Create a test user with staff status
        self.staff_user = User.objects.create_user(username='staff_user', password='password', is_staff=True)
        # Create a test user without staff status
        self.normal_user = User.objects.create_user(username='normal_user', password='password')

    # def test_authenticated_staff_user(self):
    #     # Log in the staff user
    #     self.client.login(username='staff_user', password='password')
    #     response = self.client.get(reverse('staff_view'))
    #     # Assuming 'staff_view' renders a template with the string 'Staff View' for demonstration purposes
    #     self.assertContains(response, 'Staff View')
    #     self.assertEqual(response.status_code, 200)

    # def test_authenticated_non_staff_user(self):
    #     # Log in the non-staff user
    #     self.client.login(username='normal_user', password='password')
    #     response = self.client.get(reverse('staff_view'))
    #     # Assuming 'user_view' is the URL name for the user view to which non-staff users should be redirected
    #     self.assertRedirects(response, reverse('user_view'))
    #     self.assertEqual(response.status_code, 302)

    # def test_unauthenticated_user(self):
    #     response = self.client.get(reverse('staff_view'))
    #     # Assuming 'login' is the URL name for the login view to which unauthenticated users should be redirected
    #     self.assertRedirects(response, reverse('login'))
    #     self.assertEqual(response.status_code, 302)