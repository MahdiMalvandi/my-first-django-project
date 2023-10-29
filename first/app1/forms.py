from django import forms
from django.utils import timezone
from .models import *


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ("پیشنهاد", "پیشنهاد"),
        ("باگ", "باگ"),
    )

    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    phone = forms.CharField(max_length=12, required=True)
    title = forms.ChoiceField(choices=SUBJECT_CHOICES, required=True)


# class CommentsForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ["name", 'body']

class CommentsForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    body = forms.CharField(widget=forms.Textarea, required=True)


class AddBlogForm(forms.ModelForm):
    image = forms.ImageField(label="image", required=False)
    text = forms.CharField(required=True, widget=forms.Textarea({'cols':'auto'}))
    class Meta:
        model = Post
        fields = ["title", "text", "reading_time", "categories"]


class SearchForm(forms.Form):
    query = forms.CharField()


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=20, label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=20, label="repeat password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password2'] != cd['password']:
            raise forms.ValidationError("Passwords do not match")
        return cd['password2']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class EditAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['bio', 'job', 'photo', 'date_of_birth']

