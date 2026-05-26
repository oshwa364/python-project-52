from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.
class TestCreateUser(TestCase):
    def test_create_valid_user(self):
        url = reverse('sign_up')
        user_data = {
            'username': 'Hobbit',
            'first_name': 'Frodo',
            'last_name': 'Baggins',
            'password1': 'burden123',
            'password2': 'burden123',
        }
        users_count = User.objects.count()

        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), users_count + 1)
        self.assertEqual(
            User.objects.last().username,
            user_data['username']
        )


class TestUpdateUser(TestCase):
    fixtures = ['users.json']
    def test_update_exist_user(self):
        user2 = User.objects.get(id=2)
        self.client.force_login(user2)
        url = reverse('user_update', kwargs={'pk': 2})
        user_data = {
            'username': 'Hobbit',
            'first_name': 'Frodo',
            'last_name': 'Baggins',
        }
        users_count = User.objects.count()

        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(User.objects.count(), users_count)
        self.assertEqual(
            User.objects.get(id=2).username,
            user_data['username']
        )
        self.assertEqual(
            User.objects.get(id=2).first_name,
            user_data['first_name']
        )
        self.assertEqual(
            User.objects.get(id=2).last_name,
            user_data['last_name']
        )


class TestDeleteUser(TestCase):
    fixtures = ['users.json']
    def test_delete_exist_user(self):
        user2 = User.objects.get(id=2)
        self.client.force_login(user2)
        url = reverse('user_delete', kwargs={'pk': 2})
        users_count = User.objects.count()

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(User.objects.count(), users_count - 1)
