from django.test import TestCase, RequestFactory
from django.contrib import messages
from django.urls import reverse, resolve
from datetime import datetime, timezone
from shift import views
from shift.models import Shift, ShiftUser, group, AccountUser
from shift.views import add_shift, shift_schedule, lookup_shift, book_shift
from account.models import group, group_member

class TestShiftModels(TestCase):
    def setUp(self):
        self.sample_user = AccountUser.objects.create(username='test_user', password="testuser",)
        self.sample_group = group.objects.create(username=self.sample_user, group_name="TestGroup")
        self.start_time_utc = datetime(2023, 11, 18, 8, 0, tzinfo=timezone.utc)

    def test_shift_creation(self):
        shift = Shift.objects.create(
            group_name=self.sample_group,
            start_time=self.start_time_utc,
            num_hours=4,
            num_people=2
        )

        saved_shift = Shift.objects.get(Shift_id=shift.Shift_id)

        self.assertEqual(saved_shift.group_name, self.sample_group)
        self.assertEqual(saved_shift.start_time, self.start_time_utc)
        self.assertEqual(saved_shift.num_hours, 4)
        self.assertEqual(saved_shift.num_people, 2)

    def test_shift_user_relationship(self):
        shift = Shift.objects.create(
            group_name=self.sample_group,
            start_time=self.start_time_utc,
            num_hours=4,
            num_people=2
        )

        shift_user = ShiftUser.objects.create(shift_id=shift, user_id=self.sample_user)

        saved_shift_user = ShiftUser.objects.get(id=shift_user.id)

        self.assertEqual(saved_shift_user.shift_id, shift)
        self.assertEqual(saved_shift_user.user_id, self.sample_user)

    def test_cascade_deletion(self):
        shift = Shift.objects.create(
            group_name=self.sample_group,
            start_time=self.start_time_utc,
            num_hours=4,
            num_people=2
        )

        shift_user = ShiftUser.objects.create(shift_id=shift, user_id=self.sample_user)

        shift.delete()

        with self.assertRaises(ShiftUser.DoesNotExist):
            ShiftUser.objects.get(id=shift_user.id)

class TestUrls(TestCase):
    def test_add_shift_url_resolves(self):
        url = reverse('add')
        self.assertEqual(resolve(url).func, views.add_shift)
        url = reverse('schedule')
        self.assertEqual(resolve(url).func, views.shift_schedule)
        url = reverse('book')
        self.assertEqual(resolve(url).func, views.lookup_shift)

class TestAddShiftView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.sample_user = AccountUser.objects.create(username='test_user', password="testuser",)
        self.sample_group = group.objects.create(username=self.sample_user, group_name="TestGroup")
        self.start_time_utc = datetime(2023, 11, 18, 8, 0, tzinfo=timezone.utc)

    def test_add_shift_view_with_valid_data(self):
        data = {
            'start_time': self.start_time_utc,
            'num_hours': 4,
            'num_people': 2
        }

        request = self.factory.post('/add_shift/', data)
        request.user = self.sample_user

        response = add_shift(request)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(Shift.objects.exists())

    def test_add_shift_view_with_invalid_data(self):
        data = {}

        request = self.factory.post('/add_shift/', data)
        request.user = self.sample_user

        response = add_shift(request)

        self.assertEqual(response.status_code, 200)

        self.assertFalse(Shift.objects.exists())

class LookupShiftViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.sample_user = AccountUser.objects.create(username='test_user', password='testuser', is_staff=True)
        self.sample_user2 = AccountUser.objects.create(username='test_user2', password='testuser2', is_staff=False)
        self.sample_group = group.objects.create(username=self.sample_user, group_name='TestGroup')
        self.start_time_utc = datetime(2023, 11, 18, 8, 0, tzinfo=timezone.utc)
        self.shift = Shift.objects.create(
            group_name=self.sample_group,
            start_time=self.start_time_utc,
            num_hours=4,
            num_people=2
        )
        self.group_member = group_member.objects.create(username=self.sample_user2, group_name=self.sample_group)
        self.shift_user = ShiftUser.objects.create(shift_id=self.shift, user_id=self.sample_user2)

    def test_lookup_shift_for_staff_user(self):
        request = self.factory.get('/lookup_shift/')
        request.user = self.sample_user

        response = lookup_shift(request)
        self.assertEqual(response.status_code, 200)
        rendered_content = response.content.decode('utf-8')
        self.assertIn('container', rendered_content)
        
    def test_lookup_shift_for_non_staff_user(self):
        request = self.factory.get('/lookup_shift/')
        request.user = self.sample_user2

        response = lookup_shift(request)
        self.assertEqual(response.status_code, 200)
        rendered_content = response.content.decode('utf-8')
        self.assertIn('container', rendered_content)

    def test_lookup_shift_post_request(self):
        data = {
            'start_time': self.start_time_utc,
            'num_hours': 4,
            'num_people': 2
        }
        request = self.factory.post('/lookup_shift/', data)
        request.user = self.sample_user
        
        response = lookup_shift(request)
        
class ShiftScheduleViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.sample_user = AccountUser.objects.create(username='test_user', password="testuser", is_staff=True)
        self.sample_user2 = AccountUser.objects.create(username='test_user2', password="testuser2", is_staff=False)
        self.sample_group = group.objects.create(username=self.sample_user, group_name="TestGroup")
        self.start_time_utc = datetime(2023, 11, 18, 8, 0, tzinfo=timezone.utc)
        self.shift = Shift.objects.create(
            group_name=self.sample_group,
            start_time=self.start_time_utc,
            num_hours=4,
            num_people=2
        )
        self.group_member = group_member.objects.create(username=self.sample_user2, group_name=self.sample_group)
        self.shift_user = ShiftUser.objects.create(shift_id=self.shift, user_id=self.sample_user)

    def test_shift_schedule_for_staff_user(self):
        request = self.factory.get('/shift_schedule/')
        request.user = self.sample_user
        response = shift_schedule(request)
        self.assertEqual(response.status_code, 200)

    def test_shift_schedule_for_non_staff_user(self):
        request = self.factory.get('/shift_schedule/')
        request.user = self.sample_user2
        response = shift_schedule(request)
        self.assertEqual(response.status_code, 200)

class BookShiftViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.sample_user = AccountUser.objects.create(username='test_user', password="testuser", is_staff=False)
        self.sample_group = group.objects.create(username=self.sample_user, group_name="TestGroup")
        self.start_time_utc = datetime(2023, 11, 18, 8, 0, tzinfo=timezone.utc)
        self.shift = Shift.objects.create(
            group_name=self.sample_group,
            start_time=self.start_time_utc,
            num_hours=4,
            num_people=2
        )
        self.group_member = group_member.objects.create(username=self.sample_user, group_name=self.sample_group)
    
    def test_book_shift_success(self):
        request = self.factory.post('/book/', {'id': self.shift.pk})
        request.user = self.sample_user

        messages_to_assert = []

        # in this scenario is not error. So mock_messages_error isn't work
        # def mock_messages_error(request, message):
        #     messages_to_assert.append(message)
        # messages.error = mock_messages_error

        response = book_shift(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(messages_to_assert), 0)
    
    def test_book_shift_already_booked(self):
        ShiftUser.objects.create(shift_id=self.shift, user_id=self.sample_user)
        
        request = self.factory.post('/book/', {'id': self.shift.pk})
        request.user = self.sample_user

        messages_to_assert = []

        def mock_messages_error(request, message):
            messages_to_assert.append(message)
        messages.error = mock_messages_error

        response = book_shift(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn("You have already booked this shift", messages_to_assert)
    
    def test_book_shift_full(self):
        ShiftUser.objects.create(shift_id=self.shift, user_id=AccountUser.objects.create(username='user1'))
        ShiftUser.objects.create(shift_id=self.shift, user_id=AccountUser.objects.create(username='user2'))

        request = self.factory.post('/book/', {'id': self.shift.pk})
        request.user = self.sample_user

        messages_to_assert = []

        def mock_messages_error(request, message):
            messages_to_assert.append(message)
        messages.error = mock_messages_error

        response = book_shift(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Shift is full", messages_to_assert)
