"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$',app.views.mainpage,name='mainpage'),
    url(r'^search_info$',app.views.search_info,name='search'),
    url(r'^get_info$',app.views.get_info,name='get'),
    url(r'^login$',app.views.login,name='login'),
    url(r'^regist$',app.views.regist,name='regist'),
    url(r'^imgset$',app.views.imgset,name='imgset'),
    url(r'^like$',app.views.like,name='like'),
    url(r'^recommend$',app.views.recommend,name='recommend'),
    url(r'^favicon.ico$', RedirectView.as_view(url=r'/static/favicon.ico')),
    # Examples:
    #url(r'^home$', app.views.home, name='home'),
    #url(r'^contact$', app.views.contact, name='contact'),
    #url(r'^about', app.views.about, name='about'),
    #url(r'^login/$',
    #    django.contrib.auth.views.login,
    #    {
    #        'template_name': 'app/login.html',
    #        'authentication_form': app.forms.BootstrapAuthenticationForm,
    #        'extra_context':
    #        {
    #            'title': 'Log in',
    #            'year': datetime.now().year,
    #        }
    #    },
    #    name='login'),
    #url(r'^logout$',
    #    django.contrib.auth.views.logout,
    #    {
    #        'next_page': '/',
    #    },
    #    name='logout'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
