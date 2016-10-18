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

#IP or FQDN of your domain controller
dc_url = settings.PYADSELFSERVICE_DCFQDN

#FQDN of your Domain/Forest
domain = settings.PYADSELFSERVICE_DOMAINFQDN

#User name with at least password reset and read user property permission
domain_username = settings.PYADSELFSERVICE_USERNAME
domain_password = settings.PYADSELFSERVICE_PASS

#Base DN of the domain
base_DN = settings.PYADSELFSERVICE_BASEDN

#Please cerate this path or change it to wherever you want to store the logs. Ensure to change the owner of the folder to web server user account like www-data
logPath = settings.PYADSELFSERVICE_LOGPATH

#Path of the SSL certificate where the cert for LDAPs is stored. Refer to https://support.microsoft.com/en-in/kb/321051 for more details about enabling LDAPs on your domain.
LDAPsCert = settings.PYADSELFSERVICE_LDAPSCERT

#Feel free to format logs however you want
LOG_FILENAME = (logPath + 'logs' + time.strftime("%Y%m%d")+ '.log')
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
ldap3.utils.log.set_library_log_detail_level(ldap3.utils.log.PROTOCOL)
ldap3.utils.log.set_library_log_hide_sensitive_data(True)
tls = ldap3.Tls(local_certificate_file = LDAPsCert)

#Varriable for Making connection
server = ldap3.Server(dc_url , use_ssl=True, get_info=all, tls = tls)

#Function to validate the AD attributes of a user account. In this example, we are validating user against User Logon Name(sAMAccountName), Email ID (mail) and Job Title(title) attributes. You add any custom attributes to validate against.
def do_validate(username, mail, attr3):
  username = str(username).lower()
  mail = str(mail).lower()
  attr3 = str(attr3).lower()

#Binds session to the server and opens a connection
  try:
    conn = ldap3.Connection(server, domain_username, password = domain_password, auto_bind=True) 
  except:
    return ('Server Error. Could not connect to Domain Controller')
    try:
      conn = ldap3.Connection(server, domain_username, password = domain_password, auto_bind=True) 
    except:
      return ('Server Error. Could not connect to Domain Controller')
      try:
        conn = ldap3.Connection(server, '%s@' + domain, password = domain_password, auto_bind=True) %username
      except:
        return ('Server Error. Could not connect to Domain Controller') 
        sys.exit(0)

#Searches LDAP and validate against attributes
  try:
# Search for attribute2 from settings
    sAMAccountName_filter = '(sAMAccountName=%s)' %username
    conn.search(base_DN, sAMAccountName_filter, attributes=[PYADSELFSERVICE_ATTR2])
    e = re.search(mail, str(conn.entries))
    e = str(e.group()).lower()

# Search for attribute3 from settings
    conn.search(base_DN, sAMAccountName_filter, attributes=[settings.PYADSELFSERVICE_ATTR3])
    t = re.search(attr3, str(conn.entries))
    t = str(t.group()).lower()
    if t == attr3:
       if e == mail:
          return('YGFRafd827343wdhgFDHGFDSFGHVFSNC')
    else:
        return ('Please verify the entered values. It does not match with AD')
  except:
    return ('Wrong username. Please verify if the username entered is accurate. If you still think the username is correct, please report this error to IT Support Team')
  logging.shutdown()

def do_reset(username, newpass):
    try:
      conn = ldap3.Connection(server, domain_username, password = domain_password, auto_bind=True) 
    except:
      return ('Server Error. Could not connect to Domain Controller')
      try:
         conn = ldap3.Connection(server, domain_username, password = domain_password, auto_bind=True) 
      except:
         return ('Server Error. Could not connect to Domain Controller')
         try:
            conn = ldap3.Connection(server, '%s@' + domain, password = domain_password, auto_bind=True) %username 
         except:
            return ('Server Error. Could not connect to Domain Controller')
            sys.exit(0)

    try:
      sAMAccountName_filter = '(sAMAccountName=%s)' %username
      conn.search(base_DN, sAMAccountName_filter, attributes=['sAMAccountName'])
      user_dn = str(conn.entries)
      #Slice the output and convert it to user DN
      front = user_dn.find('C')
      back = user_dn.find('\n')
      user_cn = user_dn[front:back]
	  
	  #Finally modify the user password with the new password from resetpass form
      conn.extend.microsoft.modify_password(user_cn, newpass, old_password=None)
	  
	  #Store protocol response in varriable
      msg = str(conn.result)
      msg = msg.lower()
      if 'success' in msg:
          return ('Your password has been changed successfully. You may close this window.')
      else:
          return ('Your password could not be changed. Please verify if the password enetered comply with password policy.\nAdditional Message %s' %msg)
    except:
      return ('Error setting AD password. Please verify network connectivity from this server to Domain Controller')
      sys.exit(0)
    logging.shutdown()
