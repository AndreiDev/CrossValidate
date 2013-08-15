from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/homepage/'}),
    url(r'^job/create/','CVapp.views.job_create',name='job_create'),
    #url(r'^job/view/','CVapp.views.job_view',name='job_view'),
    #url(r'^job/delete/','CVapp.views.job_delete',name='job_delete'),
    url(r'^$', TemplateView.as_view(template_name='homepage.html'),name='homepage'),                     
    # Examples:
    # url(r'^$', 'CrossValidate.views.home', name='home'),
    # url(r'^CrossValidate/', include('CrossValidate.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
