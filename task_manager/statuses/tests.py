from task_manager.users.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Status


class TestStatus(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)


class TestCreateStatus(TestStatus):
    def test_create_valid_status(self):
        url = reverse('status_create')
        status_data = {
            'name': 'abs_new_stat',
        }
        status_count = Status.objects.count()

        response = self.client.post(url, status_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), status_count + 1)
        self.assertEqual(
            Status.objects.last().name,
            status_data['name']
        )


class TestListStatuses(TestStatus):
    def test_statuses_content(self):
        url = reverse('statuses_list')
        response = self.client.get(url)

        self.assertQuerySetEqual(
            response.context['statuses'],
            Status.objects.all(),
            ordered=False,
        )


class TestUpdateStatus(TestStatus):
    def test_update_exist_status(self):
        url = reverse('status_update', kwargs={'pk': 1})
        status_data = {
            'name': 'new_status_name',
        }

        response = self.client.post(url, status_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertEqual(
            Status.objects.get(id=1).name,
            status_data['name']
        )


class TestDeleteStatus(TestStatus):
    def test_delete_exist_status(self):
        url = reverse('status_delete', kwargs={'pk': 2})
        status_count = Status.objects.count()

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertEqual(Status.objects.count(), status_count - 1)
