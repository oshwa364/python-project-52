from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=150,
        required=False,
        label='Имя',
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        label='Фамилия',
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Имя пользователя',
        help_text='Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.',
    )
    password1 = forms.CharField(
        min_length=3,
        label='Пароль',
        widget=forms.PasswordInput,
        help_text='&#8226; Ваш пароль должен содержать как минимум 3 символа.',
    )
    password2 = forms.CharField(
        min_length=3,
        label='Подтверждение пароля',
        widget=forms.PasswordInput,
        help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.',
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        )


class UserUpdateForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length=150,
        required=False,
        label='Имя',
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        label='Фамилия',
    )
    username = forms.CharField(label='Имя пользователя')

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
        )
