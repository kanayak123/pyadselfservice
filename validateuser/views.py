from django.shortcuts import render
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.core.signing import TimestampSigner
from django.core.mail.message import EmailMessage

from urllib.parse import quote, unquote
from Crypto.Cipher import AES
from Crypto import Random
from pyotp import TOTP

from .forms import renderform, passreset, renderhome, renderotp
from .adpassreset import do_validate, do_reset
from .crypt import encrypt_val, decrypt_val


totp = TOTP('base32secret3232')
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
     tokenverify = signer.unsign(getd, max_age=300)
     if request.method == 'POST':
        form = renderform(request.POST)
        if form.is_valid():
           username = form.cleaned_data['username']
           mail = form.cleaned_data['mail']
           attr3 = form.cleaned_data['attr3']
#           attr4 = form.cleaned_data['attr4']
           output = do_validate(username, mail, attr3)
           if output == 'YGFRafd827343wdhgFDHGFDSFGHVFSNC':
             otp = totp.now()
             email = EmailMessage(subject='OTP for AD Password Reset', body='Your OTP is %s ' % otp, to=[mail])
             email.send()
             cipher_text = encrypt_val(form.cleaned_data['username'])
             data = signer.sign(cipher_text)
             return HttpResponseRedirect('/otp?key=' + quote(data))
           else:
             value = "You have entered invalid details. Please go back and try again"
             return HttpResponseServerError(template.render(Context({'exception_value': value,})))
            
     return render(request, 'index.html', {'form': renderform()})

def OTP(request):
     getd = unquote(request.GET.get('key'))
     signerverify = signer.unsign(getd, max_age=300)
     if request.method == 'POST':
        form = renderotp(request.POST)
        if form.is_valid():
           otp = totp.verify(form.cleaned_data['otp'])
           data = signer.sign(getd)
           if otp == True:
             return HttpResponseRedirect('/resetpass?key=' + quote(data))
     return render(request, 'index.html', {'form': renderotp()})

def resetpass(request):
   getd = unquote(request.GET.get('key'))
   crypted_data = signer.unsign(getd, max_age=300)
   prim_key = {'username' : getd}
   if request.method == 'POST':
      form = passreset(request.POST)
      if form.is_valid():
         decrypted_value = decrypt_val(getd)
         newpassword = form.cleaned_data['newpassword']
         confirmpassword = form.cleaned_data['confirmpassword']
         if newpassword and newpassword != confirmpassword:
            value = "Your New Password and Confirm Password did not match. Please go back and try again."
            return HttpResponseServerError(template.render(Context({'exception_value': value,})))
#            return HttpResponse('Your New Password and Confirm Password did not match. Please go back and try again.', content_type="text/plain")
         else:
            output = do_reset(decrypted_value.decode("utf-8"), form.cleaned_data['confirmpassword'])
            value = str(output)
            return HttpResponseServerError(template.render(Context({'exception_value': value,})))
#            return HttpResponse(output, content_type="text/plain")
      else:
         value = "There is some error with your request. Please consult IT Support Team."
         return HttpResponseServerError(template.render(Context({'exception_value': value,})))
 #         return HttpResponse('There is some error with your request. Please consult IT Support Team.', content_type="text/plain")
   return render(request, 'index.html', {'form': passreset(initial=prim_key)})

def server_error(request):
    # Dict to pass to template, data could come from DB query
    t = loader.get_template('exception.html')
    value = "Your session is expired. Please close this window and start over."
    return HttpResponseServerError(t.render(Context({'exception_value': value,})))
