from django import forms
from django.contrib.auth.models import User
from .models import Order

class LoginForm(forms.ModelForm):
    
    password = forms.CharField(widget = forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not User.objects.filter(username = username).exists():
            raise forms.ValidationError('Пользователь с логином {} не найден в системе'.format(username))

        user = User.objects.filter(username = username).first()

        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')

        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(forms.ModelForm):

    confirm_password = forms.CharField(widget = forms.PasswordInput)
    password = forms.CharField(widget = forms.PasswordInput)
    address = forms.CharField(required = False)
    email = forms.EmailField(required = True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Повторите пароль'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['address'].label = 'Адрес'
        self.fields['email'].label = 'Электронная почта'

    def clean_email(self):
        email = self.cleaned_data['email']
        domail = email.split('.')[-1]
        if domail in ['com', 'net']:
            raise forms.ValidationError('регистрация для домаена "{}" невозможна'.format(domail))

        if User.objects.filter(email = email).exists():
            raise forms.ValidationError('Данный почтовый адрес уже используется другим пользователем')
    
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username = username).exists():
            raise forms.ValidationError('Пользователь с никнеймом {} уже существует'.format(username))
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Порали не совпадают')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username',
                    'password',
                    'confirm_password',
                    'first_name',
                    'last_name',
                    'address',
                    'email'
                ]


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].label = 'Покупатель'

    class Meta:
        model = Order
        fields = [
            'customer',
        ]