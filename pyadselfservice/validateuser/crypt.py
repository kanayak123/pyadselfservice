__author__ = "ITSupportBLR"
__copyright__ = "Copyright 2016, iAMAmazing"
__credits__ = ["IT Support Team"]
__maintainer__ = "Amith Nayak"
__email__ = "itsupportblr@snapdeal.com"
__status__ = "Production"

import base64
from Crypto.Cipher import AES
from Crypto import Random
from django.conf import settings

my_secret = settings.PYADSELFSERVICE_CRYPTKEY

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

def encrypt_val( clear_text ):
    clear_text = pad(clear_text)
    iv = Random.new().read( AES.block_size )
    cipher = AES.new( my_secret, AES.MODE_CBC, iv )
    return base64.urlsafe_b64encode( iv + cipher.encrypt(clear_text) ) 

def decrypt_val( cipher_text ):
#    enc = base64.urlsafe_b64decode(cipher_text)
    enc = base64.urlsafe_b64decode(cipher_text)
    iv = enc[:16]
    cipher = AES.new(my_secret, AES.MODE_CBC, iv )
    return unpad(cipher.decrypt( enc[16:] ))
