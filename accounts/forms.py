from django.forms import Form, CharField, TextInput, PasswordInput, EmailInput


class LoginForm(Form):
    username = CharField(label='Username', widget=TextInput(attrs={
        'id': 'username'
    }))
    password = CharField(label='Password', widget=PasswordInput(attrs={
        'id': 'password'
    }))


class RegisterForm(Form):
    first_name = CharField(label='Firstname', widget=TextInput(attrs={
        'id': 'first_name'
    }))
    last_name = CharField(label='Lastname', widget=TextInput(attrs={
        'id': 'last_name'
    }))
    email = CharField(label='Email', widget=EmailInput(attrs={
        'id': 'email'
    }))
    username = CharField(label='Username', widget=TextInput(attrs={
        'id': 'username'
    }))

    password1 = CharField(label='Password1', widget=PasswordInput(attrs={
        'id': 'password1'
    }))
    password2 = CharField(label='Password2', widget=PasswordInput(attrs={
        'id': 'password2'
    }))
