from django import forms
from .models import ContactModel, SubscribeNow
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import user_address


class ContactFormModel(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = ['name', 'email', 'message']


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ContactFormModel(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = ["name", "email", "message"]


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = SubscribeNow
        fields = ["email"]
