from django.test import TestCase
from django.urls import reverse

class TestUrls(TestCase):
    def test_about_url(self):
        url = reverse('about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/page_about.html')  

    def test_home_url(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')  

    # def test_home_en_url(self):
    #     url = reverse('home') + '/en'
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'home/home.html')  

class TestViews(TestCase):
    def test_about_view(self):
        url = reverse('about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/page_about.html')

    def test_home_view(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')
