from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from crud.models import ClassName

class TeacherRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100)
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
    email = forms.EmailField(
        label=("Email"),
    )

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

 
    def save(self):
        user = super().save(commit = False)
        user.is_staff = True
        user.save()
        return user

class StudentRegisterForm(UserCreationForm):     
    first_name= forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=100)
 
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
    email = forms.EmailField(
        label=("Email"),
    )

   
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']

       

class ClassCode(forms.ModelForm):
    class Meta:
        model = ClassName
        fields = ['class_code']

# class UserForm(forms.ModelForm):
#     first_name= forms.CharField(max_length=100)
#     last_name = forms.CharField(max_length=50)
#     class Meta:
#         model = User
#         fields = ['first_name','last_name','username','email','password1','password2']