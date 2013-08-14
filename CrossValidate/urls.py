from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/homepage/'}),
    url(r'^$', TemplateView.as_view(template_name='homepage.html'),name='homepage'),                     
    # Examples:
    # url(r'^$', 'CrossValidate.views.home', name='home'),
    # url(r'^CrossValidate/', include('CrossValidate.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
