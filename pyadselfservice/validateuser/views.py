__author__ = "Amith Nayak (iAMAmazing)"
__copyright__ = "Copyright 2016, iAMAmazing"
__credits__ = ["Amith Nayak (iAMAmazing)"]
__license__ = "GPL"
__version__ = "3"
__maintainer__ = "Amith Nayak (iAMAmazing)"
__email__ = "kanayak123@yahoo.co.in"
__status__ = "Production"
#Refer to my blogs http://blogger.iAMAmazing.in/


from django.shortcuts import render
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.core.signing import TimestampSigner
from django.core.mail.message import EmailMessage
from django.conf import settings

from urllib.parse import quote, unquote
from Crypto.Cipher import AES
from Crypto import Random
from pyotp import TOTP, random_base32

from .forms import renderform, passreset, renderotp, renderhome
from .adpassreset import do_validate, do_reset, calc_base32
from .crypt import encrypt_val #, decrypt_val


signer = TimestampSigner()
template = loader.get_template('exception.html')

def Home(request):
   if request.method == 'POST':
      form = renderhome(request.POST)
      if form.is_valid():
         data = signer.sign('jhgdJHGuytre8764876uhghJG')
         return HttpResponseRedirect('/validateuser?token=' + quote(data))
      else:
         return HttpResponse('You must read the instructions and be ready with a compatible password. Please go back and try again', content_type="text/plain")
   return render(request, 'home.html', {'form': renderhome()})

def ADValidate(request):
     getd = unquote(request.GET.get('token'))
     tokenverify = signer.unsign(getd, max_age=int(settings.PYADSELFSERVICE_STOUT))
     if request.method == 'POST':
        form = renderform(request.POST)
        if form.is_valid():
           output = do_validate(form.cleaned_data['username'], form.cleaned_data['attr3'], form.cleaned_data['attr4'], form.cleaned_data['attr5'])
           if output == 'YGFRafd827343wdhgFDHGFDSFGHVFSNC':
             cipher_text = encrypt_val(form.cleaned_data['username'])
             data = signer.sign(cipher_text)
             return HttpResponseRedirect('/otp?key=' + quote(data))
           else:
             value = "You have entered invalid details. Please go back and try again"
             return HttpResponseServerError(template.render(Context({'exception_value': value,})))
            
     return render(request, 'index.html', {'form': renderform()})

def OTP(request):
     getd = unquote(request.GET.get('key'))
     signerverify = signer.unsign(getd, max_age=int(settings.PYADSELFSERVICE_STOUT))
     if request.method == 'POST':
        form = renderotp(request.POST)
        if form.is_valid():
           base32 = calc_base32(signerverify)
           totp = TOTP(base32)
           otp = totp.verify(form.cleaned_data['otp'], valid_window=5)
           data = signer.sign(signerverify)
           if otp == True:
             return HttpResponseRedirect('/resetpass?key=' + quote(data))
     return render(request, 'index.html', {'form': renderotp()})

def resetpass(request):
   getd = unquote(request.GET.get('key'))
   crypted_data = signer.unsign(getd, max_age=int(settings.PYADSELFSERVICE_STOUT))
   prim_key = {'username' : getd}
   if request.method == 'POST':
      form = passreset(request.POST)
      if form.is_valid():
         base32 = calc_base32(crypted_data)
         newpassword = form.cleaned_data['newpassword']
         confirmpassword = form.cleaned_data['confirmpassword']
         if newpassword and newpassword != confirmpassword:
            value = "Your New Password and Confirm Password did not match. Please go back and try again."
            return HttpResponseServerError(template.render(Context({'exception_value': value,})))
         else:
            output = do_reset(crypted_data, form.cleaned_data['confirmpassword'])
            if 'success' in output:
               value = str(output)
               return HttpResponseServerError(loader.get_template('success.html').render(Context({'exception_value': value,})))
            else:
               value = str(output)
               return HttpResponseServerError(template.render(Context({'exception_value': value,})))
      else:
         value = "Your new password does not comply with password policy. Please go back and try again."
         return HttpResponseServerError(template.render(Context({'exception_value': value,})))
   return render(request, 'resetpass.html', {'form': passreset(initial=prim_key)})

def server_error(request):
    t = loader.get_template('exception.html')
    value = "Your session is expired. Please close this window and start over."
    return HttpResponseServerError(t.render(Context({'exception_value': value,})))
