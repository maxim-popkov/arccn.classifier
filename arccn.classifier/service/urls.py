from django.conf.urls import patterns, url

urlpatterns = patterns('service.views',
    url(r'^service/$', 'doc_list'),
    url(r'^service/(?P<pk>[0-9]+)$', 'doc_detail'),
    url(r'^service/(?P<pk>[0-9]+)/txt/$', 'txt_list'),
)