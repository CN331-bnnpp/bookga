from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.test import TestCase, Client
from account.models import AccountUser, group, group_member

# test for account/views.py create_member
class CreateMemberTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = AccountUser.objects.create_user(username="test", password="test")
        self.user.save()
        self.client.login(username="test", password="test")
        self.group = group.objects.create(name=self.user, group_name="test")
        self.group.save()
        self.group_member = group_member.objects.create(user=self.user, group=self.group)
        self.group_member.save()
        
    def test_create_member(self):
        request = self.factory.post(reverse("account:create_member"), {"username": "test", "group": "test"})
        request.user = self.user
        response = self.client.post(reverse("account:create_member"), {"username": "test", "group": "test"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(group_member.objects.count(), 2)
        
    def test_create_member_invalid(self):
        request = self.factory.post(reverse("account:create_member"), {"username": "test", "group": "test"})
        request.user = self.user
        response = self.client.post(reverse("account:create_member"), {"username": "test", "group": "test"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(group_member.objects.count(), 2)
        
    def test_create_member_invalid_user(self):
        request = self.factory.post(reverse("account:create_member"), {"username": "test", "group": "test"})
        request.user = self.user
        response = self.client.post(reverse("account:create_member"), {"username": "test", "group": "test"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(group_member.objects.count(), 2)
        
    def test_create_member_invalid_group(self):
        request = self.factory.post(reverse("account:create_member"), {"username": "test", "group": "test"})
        request.user = self.user
        response = self.client.post(reverse("account:create_member"), {"username": "test", "group": "test"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(group_member.objects.count(), 2)
        
    def test_create_member_invalid_user_group(self):
        request = self.factory.post(reverse("account:create_member"), {"username": "test", "group": "test"})
        request.user = self.user
        response = self.client.post(reverse("account:create_member"), {"username": "test", "group": "test"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(group_member.objects.count(), 2)
        
    def test_create_member_invalid_user_group_duplicate(self):
        request = self.factory.post(reverse("account:create_member"), {"username": "test", "group": "test"})
        request.user = self.user
        response = self.client.post(reverse("account:create_member"), {"username": "test", "group": "test"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(group_member.objects.count(), 2)
        
    def test_create_member_invalid_user_group_duplicate(self):
        request = self.factory.post(reverse("account:create_member"), {"username": "test", "group": "test"})
        request.user = self.user
        response = self.client.post(reverse("account:create_member"), {"username": "test", "group": "test"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(group_member.objects.count(), 2)
        
    def test_create_member_invalid_user_group_duplicate(self):
        request = self.factory.post(reverse("account:create_member"), {"username": "test", "group": "test"})
        request.user = self.user
        response = self.client.post(reverse("account:create_member"), {"username": "test", "group": "test"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(group_member.objects.count(), 2)
        
    def test_create_member_invalid_user_group_duplicate(self):
        request = self.factory.post(reverse("account:create_member"), {"username": "test", "group": "test"})
        request.user = self.user
        response = self.client.post(reverse("account:create_member"), {"username": "test", "group": "test"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(group_member.objects.count(), 2)
        
    def test_create_member_invalid_user_group_duplicate(self):
        request = self.factory.post(reverse("account:create_member"), {"username": "test", "group": "test"})
        request.user = self.user
        response = self.client.post(reverse("account:create_member"), {"username": "test", "group": "test"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(group_member.objects.count(), 2)
        
#

    