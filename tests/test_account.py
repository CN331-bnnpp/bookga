# Django test coverage for the account app
#
# Path: tests/test_account.py
from django.test import TestCase
from django.urls import reverse
from account.models import AccountUser, group, group_member



class AccountUserTest(TestCase):

    def test_create_user(self):
        self.user = AccountUser.objects.create_user(
            username="testuser",
            password="testuser",
        )
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "")
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        
    def test_create_superuser(self):
        self.admin_user = AccountUser.objects.create_superuser(
            username="adminuser",
            password="adminuser",
            is_staff=True,
            is_superuser=True,
        )
        self.assertEqual(self.admin_user.username, "adminuser")
        self.assertEqual(self.admin_user.email, "")
        self.assertTrue(self.admin_user.is_staff)
        self.assertTrue(self.admin_user.is_superuser)
        
    def test_create_staff(self):
        self.staff_user = AccountUser.objects.create_user(
            username="staffuser",
            password="staffuser",
            is_staff=True,
        )
        self.assertEqual(self.staff_user.username, "staffuser")
        self.assertEqual(self.staff_user.email, "")
        self.assertTrue(self.staff_user.is_staff)
        self.assertFalse(self.staff_user.is_superuser)
            
class GroupMemberTest(TestCase):
    
    def setUp(self):
        self.user = AccountUser.objects.create_user(
            username="testuser",
            password="testuser",
        )
        self.staff_user = AccountUser.objects.create_user(
            username="staffuser",
            password="staffuser",
            is_staff=True,
        )
        self.group = group.objects.create(
            username=self.staff_user,
            group_name="testgroup",
        )
        self.group_member = group_member.objects.create(
            username=self.user,
            group_name=self.group,
        )
        
    def test_create_group_member(self):
        self.assertEqual(self.group_member.username.username, "testuser")
        self.assertEqual(self.group_member.group_name.group_name, "testgroup")
        
class AccountViewsTest(TestCase):
        
        def setUp(self):
            self.user = AccountUser.objects.create_user(
                username="testuser",
                password="testuser",
                is_staff=False,
            )
            self.staff_user = AccountUser.objects.create_user(
                username="staffuser",
                password="staffuser",
                is_staff=True,
            )
            self.admin_user = AccountUser.objects.create_superuser(
                username="adminuser",
                password="adminuser",
                is_staff=True,
                is_superuser=True,
            )
            self.group = group.objects.create(
                username=self.staff_user,
                group_name="testgroup",
            )
            self.group_member = group_member.objects.create(
                username=self.user,
                group_name=self.group,
            )
            
        def test_signup(self):
            response = self.client.get(reverse("signup"))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "account/signup.html")
            data = {
                "username": "testuser2",
                "password1": "teat$222@bookga",
                "password2": "teat$222@bookga",
                "group_name": "testgroup2",
            } 
            response = self.client.post(reverse("signup"), data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(AccountUser.objects.count(), 4)
            self.assertEqual(group.objects.count(), 2)
            self.assertEqual(group_member.objects.count(), 1)
            self.assertEqual(group.objects.get(group_name="testgroup2").username.username, "testuser2")
            self.client.logout()
            data = {
                "username": "testuser3",
                "password1": "teat",
                "password2": "teat",
                "group_name": "testgroup3",
            }
            response = self.client.post(reverse("signup"), data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(AccountUser.objects.count(), 4)
            self.assertEqual(group.objects.count(), 2)
            self.assertEqual(group_member.objects.count(), 1)
            
        def test_login(self):
            response = self.client.get(reverse("login"))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "account/login.html")
            response = self.client.post(reverse("login"), {
                "username": "testuser",
                "password1": "testuser",
            })
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "account/user.html")
            response = self.client.get(reverse("login"))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "account/user.html")
            self.client.logout()
            response = self.client.post(reverse("login"), {
                "username": "staffuser",
                "password1": "staffuser",
            })
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "account/staff.html")
            self.client.logout()
            response = self.client.post(reverse("login"), {
                "username": "adminuser",
                "password1": "adminuser",
            })
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "account/admin.html")
            self.client.logout()
            response = self.client.post(reverse("login"), {
                "username": "testuser",
                "password1": "wrongpassword",
            })
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "account/login.html")
            
        def test_logout(self):
            self.client.login(username="testuser", password="testuser")
            response = self.client.get(reverse("logout"))
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("home"))
            self.client.logout()
            self.client.login(username="staffuser", password="staffuser")
            response = self.client.get(reverse("logout"))
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("home"))
            self.client.logout()
            self.client.login(username="adminuser", password="adminuser")
            response = self.client.get(reverse("logout"))
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("home"))
            
        def test_create_member(self):
            self.client.login(username="staffuser", password="staffuser")
            response = self.client.get(reverse("create"))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "account/create_member.html")
            data = {
                "username": "testuser2",
                "password1": "teat$222@bookga",
                "password2": "teat$222@bookga",
                "group_name": "testgroup2",
            }
            response = self.client.post(reverse("create"), data)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "account/create_member.html")
            self.assertEqual(group_member.objects.count(), 2)
            self.client.logout()
            
        
        
        
    
