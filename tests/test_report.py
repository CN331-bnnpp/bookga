from django.test import TestCase
from django.urls import reverse, resolve
from datetime import datetime, timezone
from report import views
from shift.models import ShiftUser
from report.views import report, countDay, countMonth
from shift.models import Shift, ShiftUser, group, AccountUser
from account.models import group, group_member
import pandas as pd

class ReportUrlsTest(TestCase):
    # test url path - report/report.html
    def test_report_url_resolves(self):
        url = reverse('report')
        self.assertEqual(resolve(url).func, views.report)

class ReportViewsTest(TestCase):
    def setUp(self):
        # create AccountUser, group, group_member, Shift, ShiftUser instances for testing
        staff_user = AccountUser.objects.create(username='staff', is_staff=True)
        non_staff_user = AccountUser.objects.create(username='user', is_staff=False)

        staff_group = group.objects.create(username=staff_user, group_name='staff_group')
        user_group = group.objects.create(username=staff_user, group_name='user_group')

        group_member_1 = group_member.objects.create(username=non_staff_user, group_name=staff_group)
        group_member_2 = group_member.objects.create(username=non_staff_user, group_name=user_group)

        self.shift = Shift.objects.create(
            group_name=staff_group,
            start_time=datetime(2023, 11, 18, 8, 0, tzinfo=timezone.utc),
            num_hours=8,
            num_people=5
        )

        self.shift_user = ShiftUser.objects.create(shift_id=self.shift, user_id=non_staff_user)

    def test_report_view(self):
        # test report funtion in report/views.py
        response = self.client.get(reverse('report'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report/report.html')

        self.assertIn('countDay', response.context)
        self.assertIn('countMonth', response.context)

class CountDayViewsTest(TestCase):
    def test_count_day(self):
        # test countDay funtion in report/views.py
        data = {
            'day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Thu'],
            'id': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        }

        df = pd.DataFrame(data)
        result = countDay(df)
        expected_output = {'Mon': 2, 'Tue': 2, 'Wed': 1, 'Thu': 2, 'Fri': 1, 'Sat': 1, 'Sun': 1}
        self.assertDictEqual(result, expected_output)

    def test_count_day_empty_data(self):
        # test countDay funtion in report/views.py with empty data with columns 'day' and 'id'
        empty_df = pd.DataFrame(columns=['day', 'id'])
        result = countDay(empty_df)
        expected_output = {'Mon': 0, 'Tue': 0, 'Wed': 0, 'Thu': 0, 'Fri': 0, 'Sat': 0, 'Sun': 0}
        self.assertDictEqual(result, expected_output)

class CountMonthViewsTest(TestCase):
    def test_count_month(self):
        # test countMonth funtion in report/views.py
        data = {
            'month': ['Jan', 'Feb', 'Mar', 'Mar', 'Apr', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            'id': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # Sample data for 'id', assuming it's a column in the DataFrame
        }

        df = pd.DataFrame(data)
        result = countMonth(df)
        expected_output = {
            'Jan': 1, 'Feb': 1, 'Mar': 2, 'Apr': 2, 'May': 1, 'Jun': 1, 'Jul': 1, 'Aug': 1, 'Sep': 1, 'Oct': 1, 'Nov': 1, 'Dec': 1
        }

        self.assertDictEqual(result, expected_output)

    def test_count_month_empty_dataframe(self):
        # test countDay funtion in report/views.py with empty data with columns 'month' and 'id'
        empty_df = pd.DataFrame(columns=['month', 'id'])
        result = countMonth(empty_df)
        expected_output = {
            'Jan': 0, 'Feb': 0, 'Mar': 0, 'Apr': 0, 'May': 0, 'Jun': 0, 'Jul': 0, 'Aug': 0, 'Sep': 0, 'Oct': 0, 'Nov': 0, 'Dec': 0
        }
        self.assertDictEqual(result, expected_output)