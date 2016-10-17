"""pyadselfservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth.views import login

from validateuser import views

handler500 = views.server_error

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.Home, name='Index0View'),
    url(r'^validateuser$', views.ADValidate, name='Index1View'),
    url(r'^otp$', views.OTP, name='Index3View'),
    url(r'^resetpass$',views.resetpass, name='Index4View'),
#    url(r'^accounts/login/$', 'login', kwargs={'authentication_form': OTPAuthenticationForm}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
