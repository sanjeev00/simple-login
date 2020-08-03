

from django import forms
from django.core.validators import RegexValidator


phone_regex = RegexValidator(regex=r'^[6789]\d{9}$', message="Phone number must be 10 digits long and start with 6,7,8,9")
name_regex = RegexValidator(regex=r'^[a-z A-Z 0-9]*$' ,message="Name cannot contain symbols")
class RegForm(forms.Form):

    name = forms.CharField( validators=[name_regex],max_length=50)
    email = forms.EmailField()
    phone = forms.CharField(validators=[phone_regex], max_length=10)

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)

class FinalForm(forms.Form):
    name = forms.CharField(validators=[name_regex], max_length=50)

class Login(forms.Form):
    phone = forms.CharField(validators=[phone_regex], max_length=10)