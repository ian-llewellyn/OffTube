from django.conf.urls import patterns, url

from offtube import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
