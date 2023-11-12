from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.test.client import Client
from django.contrib.auth.forms import UserCreationForm
from account.forms import CreateAccountForm
from account.views import signup, create_member, logout_app
from account.models import group, group_member
from django.core.exceptions import ValidationError
from account.models import AccountUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib import messages

class TestUrls(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = AccountUser.objects.create_user(username='testuser', password='testpassword')

    def test_index_url(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_login_app_url(self):
        response = self.client.get(reverse('login'), {'user': 'testuser'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gate/gate.html')

    def test_signup_url(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')

    def test_create_member_url(self):
        url = reverse('create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/create_member.html')

class TestView(TestCase):
    def setUp(self):
        self.user = AccountUser.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

    def test_index_view(self):
        # Get the URL for the index view
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        expected_count = AccountUser.objects.count()
        self.assertContains(response, str(expected_count), html=False)

        self.assertTemplateUsed(response, 'account/types.html')

    # def test_authenticated_user_redirect(self):
    #     # Log in the user
    #     self.client.login(username='testuser', password='testpassword')
    #     response = self.client.get(reverse('/login'))
    #     self.assertTemplateUsed(response, 'account/user.html')

    def test_get_request(self):
        # Make a GET request to login_app view
        response = self.client.get(reverse('login'), {'user': 'testuser'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')
    
#     def test_valid_login(self):
#         # Make a POST request to login_app view with valid credentials
#         response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
#         self.assertTemplateUsed(response, 'account/user.html')

#     def test_invalid_login(self):
#         # Make a POST request to login_app view with invalid credentials
#         response = self.client.post(reverse('login'), {'username': 'invaliduser', 'password': 'invalidpassword'})
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Invalid username and/or password.")

#     def test_render_login_user(self):
#         # Log in the user
#         self.client.login(username='testuser', password='testpassword')
#         response = self.client.get(reverse('login'), {'user': 'testuser'})
#         self.assertTemplateUsed(response, 'account/user.html')

#     def test_render_login_staff(self):
#         # Set the user as staff
#         self.user.is_staff = True
#         self.user.save()
#         self.client.login(username='testuser', password='testpassword')
#         response = self.client.get(reverse('login'), {'user': 'testuser'})
#         self.assertTemplateUsed(response, 'account/staff.html')
    
#     def test_render_login_admin(self):
#         # Set the user as admin
#         self.user.is_superuser = True
#         self.user.save()
#         self.client.login(username='testuser', password='testpassword')
#         response = self.client.get(reverse('login'), {'user': 'testuser'})
#         self.assertTemplateUsed(response, 'account/admin.html')

#     def test_get_signup_form(self):
#         # Make a GET request to signup view
#         response = self.client.get(reverse('signup'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'account/signup.html')
#         self.assertIsInstance(response.context['form'], UserCreationForm)

# class SignupViewTest(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()

#     def test_get_request(self):
#         request = self.factory.get(reverse('signup'))
#         response = signup(request)

#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, '<form')
#         self.assertContains(response, 'name="username"')
#         self.assertContains(response, 'name="password1"')
#         self.assertContains(response, 'name="password2"')

#     # def test_signup_view_POST_valid_form(self):

#     # def test_signup_view_POST_invalid_form(self):

# class GroupModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Create a user with is_staff set to True
#         cls.staff_user = AccountUser.objects.create_user(username='staff_user', password='password', is_staff=True)

#     def setUp(self):
#         # Create a group for testing
#         self.test_group = group.objects.create(username=self.staff_user, group_name='TestGroup')

#     def test_group_constraints(self):
#         # Test that the group_name cannot be empty
#         empty_group = group(username=self.staff_user, group_name='')
        
#         with self.assertRaises(ValidationError) as cm:
#             empty_group.full_clean()

#         error_dict = cm.exception.error_dict
#         self.assertIn('group_name', error_dict)
#         self.assertEqual(error_dict['group_name'][0].code, 'blank')

# class CreateMemberViewTest(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.client = Client()

#     def test_create_member_view_GET(self):
#         response = self.client.get(reverse('create'))

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'account/create_member.html')
#         self.assertIn('form', response.context)
#         self.assertIsInstance(response.context['form'], UserCreationForm)

# class GroupMemberModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Create a user with is_staff set to False
#         cls.normal_user = AccountUser.objects.create_user(username='normal_user', password='password', is_staff=False)

#         # Create a group
#         cls.test_group = group.objects.create(username=cls.normal_user, group_name='TestGroup')

# class CreateAccountFormTest(TestCase):
#     def test_save_method_creates_user(self):
#         # Create form data
#         form_data = {
#             'username': 'testuser',
#             'email': 'testuser@example.com',
#             'password1': 'TestPassword123!',
#             'password2': 'TestPassword123!',
#         }

#         form = CreateAccountForm(data=form_data)
#         self.assertTrue(form.is_valid())
#         user = form.save()

#         self.assertIsInstance(user, AccountUser)
#         self.assertTrue(AccountUser.objects.filter(username='testuser').exists())

#     def test_save_method_does_not_commit_when_commit_is_false(self):
#         # Create form data
#         form_data = {
#             'username': 'testuser',
#             'email': 'testuser@example.com',
#             'password1': 'TestPassword123!',
#             'password2': 'TestPassword123!',
#         }
#         form = CreateAccountForm(data=form_data)
#         self.assertTrue(form.is_valid())
#         user = form.save(commit=False)
#         self.assertIsInstance(user, AccountUser)
#         self.assertFalse(AccountUser.objects.filter(username='testuser').exists())
#         user.save()
#         self.assertTrue(AccountUser.objects.filter(username='testuser').exists())