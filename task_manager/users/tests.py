from task_manager.users.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse


class TestUser(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.users_count = User.objects.count()


class TestCreateUser(TestUser):
    def test_create_valid_user(self):
        url = reverse('sign_up')
        user_data = {
            'username': 'Hobbit',
            'first_name': 'Frodo',
            'last_name': 'Baggins',
            'password1': 'burden123',
            'password2': 'burden123',
        }

        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), self.users_count + 1)
        self.assertEqual(
            User.objects.last().username,
            user_data['username']
        )

    def test_create_missing_username(self):
        url = reverse('sign_up')
        user_data = {
            'username': '',
            'password1': 'burden123',
            'password2': 'burden123',
        }

        response = self.client.post(url, user_data)

        self.assertEqual(
            ['Обязательное поле.'],
            response.context['form'].errors['username']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.users_count)

    def test_create_invalid_username(self):
        url = reverse('sign_up')
        user_data = {
            'username': 'M!cky',
            'password1': '1M2i3n4i',
            'password2': '1M2i3n4i',
        }

        response = self.client.post(url, user_data)

        self.assertEqual(
            ['Введите правильное имя пользователя. '
            'Оно может содержать только буквы, цифры и знаки @/./+/-/_.'],
            response.context['form'].errors['username']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.users_count)

    def test_create_exist_username(self):
        url = reverse('sign_up')
        user1 = User.objects.get(id=1)
        user_data = {
            'username': user1.username,
            'password1': '1M2i3n4i',
            'password2': '1M2i3n4i',
        }

        response = self.client.post(url, user_data)

        self.assertEqual(
            ['Пользователь с таким именем уже существует.'],
            response.context['form'].errors['username']
        )

    def test_create_long_username(self):
        url = reverse('sign_up')
        user1 = User.objects.get(id=1)
        user_data = {
            'username': user1.username * 50,
            'password1': '1M2i3n4i',
            'password2': '1M2i3n4i',
        }

        response = self.client.post(url, user_data)

        self.assertEqual(
            ['Убедитесь, что это значение содержит не более 150 символов '
            f'(сейчас {len(user_data['username'])}).'],
            response.context['form'].errors['username']
        )

    def test_create_missing_password(self):
        url = reverse('sign_up')
        user_data = {
            'username': 'Micky',
            'password1': '',
            'password2': '',
        }

        response = self.client.post(url, user_data)

        self.assertEqual(
            ['Обязательное поле.'],
            response.context['form'].errors['password1']
        )
        self.assertEqual(
            ['Обязательное поле.'],
            response.context['form'].errors['password2']
        )

    def test_create_passwords_dont_match(self):
        url = reverse('sign_up')
        user_data = {
            'username': 'Micky',
            'password1': 'asdqwe123',
            'password2': '123qweasd',
        }

        response = self.client.post(url, user_data)

        self.assertEqual(
            ['Введенные пароли не совпадают.'],
            response.context['form'].errors['password2']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.users_count)


class TestListUsers(TestUser):
    def test_users_content(self):
        url = reverse('users_list')

        response = self.client.get(url)

        self.assertQuerySetEqual(
            response.context['users'],
            User.objects.all(),
            ordered=False,
        )


class TestUpdateUser(TestUser):
    def test_update_self(self):
        user2 = User.objects.get(id=2)
        self.client.force_login(user2)
        url = reverse('user_update', kwargs={'pk': 2})
        user_data = {
            'username': 'Hobbit',
            'first_name': 'Frodo',
            'last_name': 'Baggins',
        }

        response = self.client.post(url, user_data)
        user2 = User.objects.get(id=2)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(User.objects.count(), self.users_count)
        self.assertEqual(
            user2.username,
            user_data['username']
        )
        self.assertEqual(
            user2.first_name,
            user_data['first_name']
        )
        self.assertEqual(
            user2.last_name,
            user_data['last_name']
        )

    def test_update_other(self):
        user2 = User.objects.get(id=2)
        self.client.force_login(user2)
        url = reverse('user_update', kwargs={'pk': 1})
        user_data = {
            'username': 'Hobbit',
            'first_name': 'Frodo',
            'last_name': 'Baggins',
        }

        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 302)        
        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(User.objects.count(), self.users_count)
        self.assertNotEqual(
            User.objects.get(id=1).username,
            user_data['username']
        )


class TestDeleteUser(TestUser):
    def test_delete_self(self):
        user2 = User.objects.get(id=2)
        self.client.force_login(user2)
        url = reverse('user_delete', kwargs={'pk': 2})

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(User.objects.count(), self.users_count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(id=2)

    def test_delete_other(self):
        user2 = User.objects.get(id=2)
        self.client.force_login(user2)
        url = reverse('user_delete', kwargs={'pk': 1})

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(User.objects.count(), self.users_count)
