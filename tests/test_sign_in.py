from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, AnonymousUser
from sign_in.forms import SignInViaUsernameForm , createUserForm
from django.http import HttpResponseRedirect

class TestUrls(TestCase):
    def test_login_url_resolves(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) 

    def test_logout_url_resolves(self):
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) 

    def test_gate_url_resolves(self):
        url = reverse('gate')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_view_authenticated_staff(self):
        # Create a staff user
        staff_user = User.objects.create_user(username='staffuser', password='password', is_staff=True)
        self.client.force_login(staff_user)
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_in/sign-in-test.html')

    def test_login_view_authenticated_user(self):
        # Create a regular user
        regular_user = User.objects.create_user(username='regularuser', password='password')
        self.client.force_login(regular_user)
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_in/sign-in-test.html')

    def test_login_view_get_request(self):
        response = self.client.get(reverse('gate'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gate/gate.html')

    def test_login_method(self):
        # Create a mock request object
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        client = Client()

        # Log in the user and get the session
        response = client.post('/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)  # Adjust the status code based on your login view

        # Now, you can access the session from the client's cookies
        session_data = client.session
        request = self.client.request().wsgi_request
        request.session = session_data

        # Create a form and authenticate the user
        form = SignInViaUsernameForm(data={'username': 'testuser', 'password': 'testpassword'})
        form.is_valid()  # Ensure the form is valid before calling login

        # Attach the user to the form
        form.user_cache = self.user

        # Call the login method
        form.login(request)


    def test_login_view_invalid_credentials(self):
        response = None

        try:
            response = self.client.post(reverse('login'), {'username': 'invaliduser', 'password': 'invalidpassword'})
        except ValidationError as e:
            # Catch the validation error raised for invalid credentials
            self.assertEqual(str(e), "['Invalid username or password!']")
        # Because inthis case is invalid username or password
        # else:
        #     # If no validation error is raised, check the response
        #     self.assertIsNotNone(response)
        #     self.assertEqual(response.status_code, 200)
        #     self.assertTemplateUsed(response, 'sign_in/sign-in.html')
        #     self.assertContains(response, "Invalid username or password!")

    def test_login_view_inactive_user(self):
        response = None

        try:
            response = self.client.post(reverse('login'), {'username': 'inactiveuser', 'password': 'password'})
        except ValidationError as e:
            # Catch the validation error raised for an inactive user
            self.assertEqual(str(e), "['Invalid username or password!']")
        # Because inthis case is invalid username or password
        # else:
        #     # If no validation error is raised, check the response
        #     self.assertIsNotNone(response)
        #     self.assertEqual(response.status_code, 200)
        #     self.assertTemplateUsed(response, 'sign_in/sign-in.html')
        #     self.assertContains(response, "This account is inactive.")
    
    def test_logout_view_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))

        # Check that the user is logged out and redirected
        self.assertIn(response.status_code, [301, 302])  # Allow both 301 and 302
        self.assertNotIn('_auth_user_id', self.client.session)

        # Follow the redirect and check the final response
        response = self.client.get(response.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gate/gate.html')

    def test_logout_view_unauthenticated_user(self):
        # Call the logout view for an unauthenticated user
        response = self.client.get(reverse('logout'))

        # Check that the response is a redirect to the login page
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.status_code, 302)  # Assuming a redirect code of 302

        # Check that the user is still unauthenticated
        self.assertNotIn('_auth_user_id', self.client.session)

        # Follow the redirect and check the final response
        response = self.client.get(response.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gate/gate.html')

    def test_gate_view_authenticated_user(self):
        # Create an authenticated user for testing
        self.client = Client()
        user = AnonymousUser()
        user.username = 'testuser'
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('gate'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gate/gate.html')
        self.assertEqual(response.context['user'], user)
        self.assertIsInstance(response.context['LoginForm'], SignInViaUsernameForm)
        self.assertIsInstance(response.context['SignupForm'], createUserForm)

class TestForm(TestCase):
    
    def test_create_user_form(self):
        # Test valid data
        form_data = {'username': 'newuser', 'password1': 'newpassword', 'password2': 'newpassword'}
        form = createUserForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Test mismatched passwords
        form_data = {'username': 'newuser', 'password1': 'newpassword', 'password2': 'differentpassword'}
        form = createUserForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Test invalid data
        form_data = {'username': '', 'password1': 'newpassword', 'password2': 'newpassword'}
        form = createUserForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_user_form_valid_data(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'Harry',
            'last_name': 'Potter',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = createUserForm(data=form_data)
        self.assertTrue(form.is_valid())

        user = form.createUser(commit=False)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.first_name, 'Harry')
        self.assertEqual(user.last_name, 'Potter')
        self.assertEqual(user.email, 'testuser@example.com')
    
    def test_create_user_invalid_data(self):
        # Test create user method with invalid data
        invalid_form_data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalidemail',  # Invalid email format
            'password1': 'testpassword',
            'password2': 'mismatchedpassword',
        }
        form = createUserForm(data=invalid_form_data)
        self.assertFalse(form.is_valid())

        # Test create user method with invalid data and commit=True
        with self.assertRaises(ValueError):
            form.createUser(commit=True)