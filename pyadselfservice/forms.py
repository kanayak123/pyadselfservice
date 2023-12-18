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
from django.conf import settings

from captcha.fields import CaptchaField

class renderhome(forms.Form):
      agreement = forms.BooleanField(required=False, widget=forms.HiddenInput)

class renderotp(forms.Form):
      otp = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}), help_text='OTP is sent to your email ID. OTP is valid for 5 mins.', required=True, label='OTP')

class renderform(forms.Form):
      username = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}), help_text='Your current AD Username', required=True, label='Username')
      attr3 = forms.CharField(required=True, label=settings.PYADSELFSERVICE_ATTR3, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
      captcha = CaptchaField()

class passreset(forms.Form):
      username = forms.CharField(required=True, widget=forms.HiddenInput(attrs={'autocomplete': 'off'})) 
      newpassword = forms.CharField(widget=forms.PasswordInput())
      confirmpassword = forms.CharField(widget=forms.PasswordInput())
