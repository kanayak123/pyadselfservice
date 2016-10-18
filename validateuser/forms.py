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
from captcha.fields import ReCaptchaField
from django.conf import settings


class renderhome(forms.Form):
      agreement = forms.BooleanField(required=True, label='I have gone through all the password policy statement. I am ready with a password that comply with this policy statement and I want to continue.  ')
      fields = ['agreement']

class renderotp(forms.Form):
      otp = forms.CharField(help_text='otp is sent to your official email ID.', required=True, label='OTP')

class renderform(forms.Form):
      username = forms.CharField(help_text='Your current AD User Name', required=True, label='Your User Name')
      mail = forms.EmailField(initial='@example.com', required=True, label='Email Address')
      attr3 = forms.CharField(required=True, label=str(settings.PYADSELFSERVICE_ATTR3))
#      dob = forms.DateField(required=True, label='Your DOB', widget=DateTimePicker(options={"format": "YYYY-MM-DD",}))
      captcha = ReCaptchaField(attrs={'theme' : 'clean'})


class passreset(forms.Form):
      username = forms.CharField(required=True, widget=forms.HiddenInput()) 
      newpassword = forms.CharField(help_text='Ensure the password is according to the password policy', widget=forms.PasswordInput, required=False, label='Your New Password')
      confirmpassword = forms.CharField(widget=forms.PasswordInput, required=False, label='Confirm Password')
      fields = ['username', 'newpassword', 'confirmpassword']
#      def clean_name(self):
#        if not self['username'].html_name in self.data:
#            return self.fields['username'].initial
#        return self.cleaned_data['username']
