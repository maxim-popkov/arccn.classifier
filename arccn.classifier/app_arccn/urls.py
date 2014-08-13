from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
       url(r'^admin/', include(admin.site.urls)),
       url(r'^', include('app_classifier.urls')),
       url(r'^i18n/', include('django.conf.urls.i18n')),
       )
