from django import forms
from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth.forms import UserCreationForm 
from .models import profile,CameraMan ,Client,Order









class LoginForm(forms.Form):
    username = forms.CharField(max_length=40)
    password = forms.CharField(max_length=40 , widget=forms.PasswordInput)
    

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class':'form-control'}))    
    class Meta:
        model = User
        fields = ['username','email']

class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','row':5}))

    class Meta:
        model = profile
        fields = ['avatar','bio']

class CreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=65)
    last_name = forms.CharField(max_length=65)
    email = forms.EmailField()
    class Meta:
        model = User
        fields=['username','password1','password2','email','first_name']

class CameraManForm(forms.ModelForm):
    class Meta:
        model = CameraMan    
        fields = '__all__' 


class CleintForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class Order_Form(forms.ModelForm):
    class Meta :
        model = Order
       
        fields = ['name','camera_men','location','client','created_by']