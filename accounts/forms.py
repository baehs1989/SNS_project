from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

    #Optional
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = 'Display Name'
        self.fields['email'].label = "Email Address"



from django import forms
from django.contrib.auth import authenticate, login, get_user_model
User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    email = forms.EmailField()

    def clean_username(self):
        username = self.cleaned_data.get('username').lower()
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is already taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is already used")
        return email

    def clear(self):
        data = self.cleaned_data
        password = data.get("password")
        password2 = data.get("password2")

        if password != password2:
            raise forms.ValidationError("Passwords must match")
        return data
