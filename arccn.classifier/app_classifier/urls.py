from django.conf.urls import patterns, url
from app_classifier import views, views_classify

urlpatterns = patterns('service.classifier.views',
    #classifiers
    url(r'^classifier/$', views.ClsList.as_view()),
    url(r'^classifier/(?P<cls_id>[0-9]+)$', views.ClsDetail.as_view()),
    url(r'^classifier/(?P<cls_id>[0-9]+)/vectors/$', views.VectorList.as_view()),
    url(r'^classifier/(?P<cls_id>[0-9]+)/labels/$', views.LabelList.as_view()),
    url(r'^classifier/(?P<cls_id>[0-9]+)/classify/$', views_classify.ClassifyList.as_view()),
)