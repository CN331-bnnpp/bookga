from django.test import TestCase
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from sign_in.forms import SignInViaUsernameForm  

class TestUrls(TestCase):
    def test_login_url_resolves(self):
        url = reverse('sign_in')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) 

    def test_logout_url_resolves(self):
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) 

    def test_gate_url_resolves(self):
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_view_authenticated_staff(self):
        # Create a staff user
        staff_user = User.objects.create_user(username='staffuser', password='password', is_staff=True)
        self.client.force_login(staff_user)
        response = self.client.get(reverse('sign_in'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_in\sign-in-test.html')

    def test_login_view_authenticated_user(self):
        # Create a regular user
        regular_user = User.objects.create_user(username='regularuser', password='password')
        self.client.force_login(regular_user)
        response = self.client.get(reverse('sign_in'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_in\sign-in-test.html')

    def test_login_view_get_request(self):
        # Make a GET request to the login view
        response = self.client.get(reverse('logout')) # gate view
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gate/gate.html')

    def test_login_view_invalid_credentials(self):
        response = None

        try:
            response = self.client.post(reverse('sign_in'), {'username': 'invaliduser', 'password': 'invalidpassword'})
        except ValidationError as e:
            # Catch the validation error raised for invalid credentials
            self.assertEqual(str(e), "['Invalid username or password!']")
        else:
            # If no validation error is raised, check the response
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'sign_in/sign-in.html')
            self.assertContains(response, "Invalid username or password!")

    def test_login_view_inactive_user(self):
        response = None

        try:
            response = self.client.post(reverse('sign_in'), {'username': 'inactiveuser', 'password': 'password'})
        except ValidationError as e:
            # Catch the validation error raised for an inactive user
            self.assertEqual(str(e), "['Invalid username or password!']")
        else:
            # If no validation error is raised, check the response
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'sign_in/sign-in.html')
            self.assertContains(response, "This account is inactive.")
    
    # def test_logout_view_authenticated_user(self):
    #     test_user = User.objects.create_user(username='testuser', password='testpassword')
    #     self.client.force_login(test_user)
    #     # Make a GET request to the logout view
    #     response = self.client.get(reverse('logout'))
    #     # Check if the user is redirected to the login page
    #     self.assertRedirects(response, '/sign_in/', status_code=302) # nust be logins
    #     # Ensure that the user is not authenticated after logout
    #     self.client.session.get('_auth_user_id')

    # def test_logout_view_unauthenticated_user(self):
    #     response = self.client.get(reverse('logout'))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, '/login/')

# class FormTest(TestCase):
#     def setUp(self):
#         # Create a test user
#         self.test_user = User.objects.create_user(username='testuser', password='testpassword')
#         self.client = Client()

#     def test_sign_in_form_valid(self):
#         # Prepare valid form data
#         form_data = {'username': 'testuser', 'password': 'testpassword'}

#         # Create an instance of the SignInViaUsernameForm with the valid data
#         form = SignInViaUsernameForm(data=form_data)

#         # Check if the form is valid
#         self.assertTrue(form.is_valid())

#         # Call the login method on the form
#         form.login()

#         # Check if the user is authenticated after login
#         authenticated_user = authenticate(username='testuser', password='testpassword')
#         self.assertIsNotNone(authenticated_user)
#         self.assertEqual(authenticated_user, self.test_user)

#     def test_sign_in_form_invalid(self):
#         # Prepare invalid form data
#         form_data = {'username': 'testuser', 'password': 'wrongpassword'}

#         # Create an instance of the SignInViaUsernameForm with the invalid data
#         form = SignInViaUsernameForm(data=form_data)

#         # Check if the form is invalid
#         if form.is_valid():
#             print("Form is unexpectedly valid.")
#             print("Form errors:", form.errors)

#         # Call the login method on the form
#         form.login()

#         # Check if the user is not authenticated after an invalid login attempt
#         authenticated_user = authenticate(username='testuser', password='wrongpassword')
#         self.assertIsNone(authenticated_user)

#     def test_sign_in_view(self):
#         # Test the sign-in view with valid credentials
#         response = self.client.post(reverse('sign_in'), {'username': 'testuser', 'password': 'testpassword'})

#         # Check if the user is redirected after successful login
#         self.assertRedirects(response, reverse('home:home'))  # Update with the actual URL for the home view

#         # Check if the user is authenticated after login
#         authenticated_user = authenticate(username='testuser', password='testpassword')
#         self.assertIsNotNone(authenticated_user)
#         self.assertEqual(authenticated_user, self.test_user)

#         # Test the sign-in view with invalid credentials
#         response_invalid = self.client.post(reverse('sign_in'), {'username': 'testuser', 'password': 'wrongpassword'})

#         # Check if the user is redirected after an invalid login attempt
#         self.assertRedirects(response_invalid, reverse('login'))  # Update with the actual URL for the login view

#         # Check if the user is not authenticated after an invalid login attempt
#         authenticated_user_invalid = authenticate(username='testuser', password='wrongpassword')
#         self.assertIsNone(authenticated_user_invalid)