""" url paterns file for OffTube project. """
from django.conf.urls import patterns, url

from offtube import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^play/(?P<video_id>\d+)$', views.play, name='play'),
    url(r'^embed/(?P<video_id>\d+)$', views.play, name='embed'),
    url(r'^popular/(?P<period>\d+)?$', views.popular, name='popular'),
    url(r'^videos/(?P<username>\S+)?$', views.videos, name='videos'),
    url(r'^edit/(?P<video_id>\d+)$', views.edit, name='edit'),
    url(r'^delete/(?P<video_id>\d+)$', views.delete, name='delete'),
    url(r'^search/$', views.search, name='search'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'offtube/login.html'}, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
)
