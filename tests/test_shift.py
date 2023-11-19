from django.test import TestCase, RequestFactory, Client
from django.urls import reverse, resolve
from datetime import datetime, timezone
from shift import views
from shift.models import Shift, ShiftUser, group, AccountUser
from shift.views import add_shift, shifts_view
from account.models import group_member

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
    
    def test_str_representation(self):
        shift = Shift.objects.create(
            group_name=self.sample_group,
            start_time=self.start_time_utc,
            num_hours=4,
            num_people=2
        )
        shift_user = ShiftUser.objects.create(shift_id=shift, user_id=self.sample_user)
        expected_output = "Shift ID: Shift ID: 1, Group: TestGroup, Start Time: 2023-11-18 08:00:00+00:00, Num Hours: 4, Num People: 2, User ID: test_user"
        self.assertEqual(str(shift_user), expected_output)

class TestUrls(TestCase):
    def test_add_shift_url_resolves(self): 
        url = reverse('add') 
        self.assertEqual(resolve(url).func, views.add_shift) 

    def test_shifts_view_url(self):
        url = reverse('shifts_view') 
        self.assertEqual(resolve(url).func, views.shifts_view) 

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

class ShiftsViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = AccountUser.objects.create_user(username='test_user', password='test_password')
        self.group = group.objects.create(username=self.user, group_name='Test Group')
        # self.group_member = group_member.objects.create(username=self.user, group_name=self.group.group_name)
        self.shift = Shift.objects.create(group_name=self.group.group_name, shift_name='Morning Shift')

    def test_shifts_view_with_user_group(self):
        request = self.factory.get('/shifts/')
        request.user = self.user
        request.username = self.user.username
        request.group_name = self.group_member.group_name

        response = shifts_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Morning Shift')