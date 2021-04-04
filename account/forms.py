from django import forms
from .models import Profile , PhoneLogin

class UserLogInForm(forms.Form):
    username = forms.CharField(max_length=30 , widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password = forms.CharField(max_length=40 , widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=30 , widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = forms.EmailField(max_length=50,widget=forms.TextInput(attrs={"class":'form-control','placeholder':'Email'}))
    password = forms.CharField(max_length=40 , widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2 = forms.CharField(max_length=40 , label='Confirm password' ,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm your Password'}))


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','age' ,'phone','image']
    email = forms.EmailField()

class PhoneLoginForm(forms.ModelForm):
    class Meta:
        model = PhoneLogin
        fields = ['phone']

        widgets = {
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Please enter your phone number'})
        }

class VerifyForm(forms.Form):
    code = forms.IntegerField (widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your code ex. 1111'}))
