from django.test import TestCase
from django.urls import reverse

class AboutUrlsTest(TestCase):
    def test_about_url(self):
        # test url path - about/page_abount.html
        url = reverse('about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/page_about.html')  
    
    def test_home_url(self):
        # test url path - home/home.html
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')  

class AboutViewsTest(TestCase):
    def test_about_view(self):
        # test function about in about/views.py
        url = reverse('about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/page_about.html')

    def test_home_view(self):
        # test function home in about/views.py
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')
