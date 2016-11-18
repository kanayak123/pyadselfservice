__author__ = "Amith Nayak (iAMAmazing)"
__copyright__ = "Copyright 2016, iAMAmazing"
__credits__ = ["Amith Nayak (iAMAmazing)"]
__license__ = "GPL"
__version__ = "3"
__maintainer__ = "Amith Nayak (iAMAmazing)"
__email__ = "kanayak123@yahoo.co.in"
__status__ = "Production"
#Refer to my blogs http://blogger.iAMAmazing.in/

from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from django.conf import settings
from nocaptcha_recaptcha.fields import NoReCaptchaField

from zxcvbn_password.fields import PasswordField, PasswordConfirmationField


class renderhome(forms.Form):
      agreement = forms.BooleanField(required=False, widget=forms.HiddenInput)

class renderotp(forms.Form):
      otp = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}), help_text='otp is sent to your official email ID.', required=True, label='OTP')

class renderform(forms.Form):
      username = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}), help_text='Your current AD Username', required=True, label='Username')
      attr3 = forms.CharField(label=settings.PYADSELFSERVICE_ATTR3, widget=forms.TextInput(attrs={'autocomplete': 'off'}), required=True)
      attr4 = forms.CharField(label=settings.PYADSELFSERVICE_ATTR4,required=True, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
      attr5 = forms.CharField(label=settings.PYADSELFSERVICE_ATTR5, required=True, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
      captcha = NoReCaptchaField()

class passreset(forms.Form):
      username = forms.CharField(required=True, widget=forms.HiddenInput(attrs={'autocomplete': 'off'})) 
      newpassword = PasswordField(label='New Password',)
      confirmpassword = PasswordConfirmationField(label='Confirm Password', confirm_with='newpassword')
