## Python Active Directory Self Service (pyadselfservice)

#####pyadselfservice is a software created using Python 3.5 and Django 1.10. This project aims to provide web based password change interface to the end users, for their Active Directory account. While changing the password, users won't not need to enter their current password. Which means users can change their password even if they have forgotten their current password. Moreover, while changing the password, this software will automatically unlock the user account if it is locked. The authenticity of the user is verified against 2 factor authentication. The first factor is validation of 3 different AD attributes. User will need to provide 3 different information which only he will know such as Home Telephone, Pin Code or any new AD attribute say PIN, Date of Birth, Date of Joining etc. The second factor is One Time Password (OTP). After successful validation of First Factor, a OTP is sent to the Email address of the user, may it be official or personal.

The documentation for this software is in below link
http://blogger.iamamazing.in/2016/10/web-based-python3-password-reset-tool.html

For Support and suggestions, please create a issue on GIT https://github.com/kanayak123/pyadselfservice/issues
