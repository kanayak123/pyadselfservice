__author__ = "Amith Nayak (iAMAmazing)"
__copyright__ = "Copyright 2016, iAMAmazing"
__credits__ = ["Amith Nayak (iAMAmazing)"]
__license__ = "GPL"
__version__ = "3"
__maintainer__ = "Amith Nayak (iAMAmazing)"
__email__ = "kanayak123@yahoo.co.in"
__status__ = "Production"
#Refer to my blogs http://blogger.iAMAmazing.in/

import ldap3, sys, getpass, logging, time, ssl, re
from django.conf import settings
from os import makedirs
from django.core.mail.message import EmailMessage
from pyotp import TOTP, random_base32

ldap3.utils.log.set_library_log_detail_level(ldap3.utils.log.BASIC)
ldap3.utils.log.set_library_log_hide_sensitive_data(True)
server = ldap3.Server(host = settings.PYADSELFSERVICE_DCFQDN, port = int(settings.PYADSELFSERVICE_DCPORT), use_ssl=True, tls = ldap3.Tls(validate=ssl.CERT_NONE))

#Function to validate the AD attributes of a user account. In this example, we are validating user against User Logon Name(sAMAccountName), Email ID (mail) and Job Title(title) attributes. You add any custom attributes to validate against.
def do_validate(username, attr3, attr4, attr5):
  username = str(username).lower()

#Binds session to the server and opens a connection
  try:
    conn = ldap3.Connection(server, settings.PYADSELFSERVICE_USERNAME, password = settings.PYADSELFSERVICE_PASS, auto_bind=True) 
  except:
    return ('Server Error. Could not connect to Domain Controller')
    try:
      conn = ldap3.Connection(server, settings.PYADSELFSERVICE_USERNAME, password = settings.PYADSELFSERVICE_PASS, auto_bind=True) 
    except:
      return ('Server Error. Could not connect to Domain Controller')
      try:
        conn = ldap3.Connection(server, '%s@' + settings.PYADSELFSERVICE_DOMAINFQDN, password = settings.PYADSELFSERVICE_PASS, auto_bind=True) %username
      except:
        return ('Server Error. Could not connect to Domain Controller') 
        sys.exit(0)

#Searches LDAP and validate against attributes
  try:
# Search for attribute2 from settings
    conn.search(search_base = settings.PYADSELFSERVICE_BASEDN,
                search_filter = '(sAMAccountName=%s)' %username,
                search_scope = ldap3.SUBTREE,
                attributes = ['cn', settings.PYADSELFSERVICE_ATTR2, settings.PYADSELFSERVICE_ATTR3, settings.PYADSELFSERVICE_ATTR4, settings.PYADSELFSERVICE_ATTR5])
    attR5 = re.search(attr5, str(conn.entries))
    attR5 = str(attR5.group()).lower()
    attR4 = re.search(attr4, str(conn.entries))
    attR4 = str(attR4.group()).lower()
    attR3 = re.search(attr3, str(conn.entries))
    attR3 = str(attR3.group()).lower()
    if attR5 == attr5.lower():
       if attR4 == attr4.lower():
          if attR3 == attr3.lower():
             base32 = calc_base32(username)        
             totp = TOTP(base32)
             otp = totp.now()
             email = EmailMessage(subject='OTP for AD Password Reset', body='Your OTP is %s ' % otp, to=[str(conn.entries[0].mail.value)])
             email.send()
             return('YGFRafd827343wdhgFDHGFDSFGHVFSNC')
    else:
        return ('Please verify the entered values. It does not match with AD')
  except:
    return ('Wrong username. Please verify if the username entered is accurate. If you still think the username is correct, please report this error to IT Support Team')
#  logging.shutdown()

def do_reset(username, newpass):
    try:
      conn = ldap3.Connection(server, settings.PYADSELFSERVICE_USERNAME, password = settings.PYADSELFSERVICE_PASS, auto_bind=True) 
    except:
      return ('Server Error. Could not connect to Domain Controller')
      try:
         conn = ldap3.Connection(server, settings.PYADSELFSERVICE_USERNAME, password = settings.PYADSELFSERVICE_PASS, auto_bind=True) 
      except:
         return ('Server Error. Could not connect to Domain Controller')
         try:
            conn = ldap3.Connection(server, '%s@' + domain, password = settings.PYADSELFSERVICE_PASS, auto_bind=True) %username 
         except:
            return ('Server Error. Could not connect to Domain Controller')
            sys.exit(0)

    try:
      conn.search(search_base = settings.PYADSELFSERVICE_BASEDN,
                  search_filter = '(sAMAccountName=%s)' %username,
                  search_scope = ldap3.SUBTREE,
                  attributes = ['sAMAccountName'],
                  paged_size = 1)
      for entry in conn.response:
         user_dn = entry['dn']
         conn.extend.microsoft.unlock_account(user_dn)
         conn.extend.microsoft.modify_password(user_dn, newpass, old_password=None)
	  #Store protocol response in varriable
         msg = str(conn.result)
         msg = msg.lower()
         if 'success' in msg:
            return ('Congratulations! You\'ve successfully changed your AD password. You may close this window.')
         else:
            return ('Your password could not be changed. Please verify if the password entered comply with password policy.\nAdditional Message %s' %msg)
    except:
      return ('Error setting AD password. Please verify network connectivity from this server to Domain Controller')
      sys.exit(0)
#    logging.shutdown()

def calc_base32(username):
  conn = ldap3.Connection(server, settings.PYADSELFSERVICE_USERNAME, password = settings.PYADSELFSERVICE_PASS, auto_bind=True)
  try:
    conn.search(search_base = settings.PYADSELFSERVICE_BASEDN,
                search_filter = '(sAMAccountName=%s)' %username,
                search_scope = ldap3.SUBTREE,
                attributes = ['cn', settings.PYADSELFSERVICE_ATTR2, settings.PYADSELFSERVICE_ATTR3, settings.PYADSELFSERVICE_ATTR4, settings.PYADSELFSERVICE_ATTR5])
    string = re.sub('[^a-zA-Z2-7]', '', str(conn.entries))
    base32 = str(string).upper()[:16]
    return base32
    sys.exit(0)
  except:
    return ('26GN6OWO5F3KX4QU')
    sys.exit(0)
