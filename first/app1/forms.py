from django import forms
from django.utils import timezone
from .models import *
from django.contrib.auth.forms import AuthenticationForm

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
    password = forms.CharField(max_length=20, label=False, widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Your Password'
    }))
    password2 = forms.CharField(max_length=20, label=False, widget=forms.PasswordInput(attrs={
        'placeholder':'Enter The Repeat Password '
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
                  'username':False,
                   'first_name':False,
                   'last_name':False,
                   'email':False
                  }
        widgets = {
            'username':forms.TextInput(attrs={
                
                'placeholder': 'Enter Your Username'
            }),
            'first_name':forms.TextInput(attrs={
                'placeholder': 'Enter Your First Name'
            }),
            'last_name':forms.TextInput(attrs={
                'placeholder': 'Enter Your Last Name'
            }),
            'email':forms.TextInput(attrs={
                'placeholder': 'Enter Your Email'
            })
        }

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


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":'Enter Your Username'}),label=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":'Enter Your Password'}),label=False)
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid username or password")
        return username