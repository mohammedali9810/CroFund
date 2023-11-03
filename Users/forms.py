from django import forms
from django.db import models
from django.contrib.auth import authenticate,get_user_model
from .models import *
from django.contrib.auth.forms import UserCreationForm



class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":"USERNAME"}))
    email = forms.EmailField(label="",widget=forms.TextInput(attrs={"placeholder":"EMAIL ADDRESS"}))
    password1 = forms.CharField(label="",widget=forms.PasswordInput(attrs={"placeholder":"PASSWORD"}))
    password2 = forms.CharField(label="",widget=forms.PasswordInput(attrs={"placeholder":"CONFIRM PASSWORD"}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class UserProfile(forms.ModelForm):
    phone = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":"phone"}),max_length=12,validators = [ RegexValidator(regex='^01[0|1|2|5][0-9]{8}$',message='Phone must be start 010, 011, 012, 015 and all number contains 11 digits',code='invalid number') ])
    image = forms.ImageField(label="")
    class Meta:
        model = Profile
        fields = ['phone','image']



class userLogin(forms.Form):
    username = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":"Enter username"}))
    password = forms.CharField(label="",widget=forms.PasswordInput(attrs={"placeholder":"Password"}))


    def clean(self,*args,**kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError("The user not exist")
            if not user.check_password(password):
                raise forms.ValidationError("the password not correct")
        return super(userLogin, self).clean(*args,**kwargs)

