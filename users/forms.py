from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from crud.models import ClassName
from users.models import Profile


class TeacherRegisterForm(UserCreationForm):
    first_name= forms.CharField(max_length=50,required=True)
    last_name = forms.CharField(max_length=50,required=True)   
    username = forms.CharField(label=('Username'),max_length=50,required=True)
    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    def clean(self):
        cleaned_data = super().clean()
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')


    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']

 
    def save(self):
        user = super().save(commit = False)
        user.is_staff = True
        user.save()
        return user

class StudentRegisterForm(UserCreationForm):     
    first_name= forms.CharField(label=('Firstname'),max_length=50,required=True)
    last_name = forms.CharField(label=('Lastname'),max_length=50,required=True)
    username = forms.CharField(label=('Username'),max_length=50,required=True)
 
 
    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    def clean(self):
        cleaned_data = super().clean()
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        

    def __init__(self, *args, **kwargs):
        super(StudentRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']

       

class ClassCode(forms.ModelForm):
    class Meta:
        model = ClassName
        fields = ['class_code']

class UserUpdateForm(forms.ModelForm):
    first_name= forms.CharField(label=('Firstname'),max_length=50,required=True)
    last_name = forms.CharField(label=('Lastname'),max_length=50,required=True)
    username = forms.CharField(label=('Username'),max_length=50,required=True)
 
 
    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']

class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(max_length=255,widget=forms.Textarea(attrs={'rows':2}))
    class Meta:
        model = Profile
        fields =['bio','profile_image']
