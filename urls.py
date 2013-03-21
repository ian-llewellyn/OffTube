from django.conf.urls import patterns, url

from offtube import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    #url(r'^(?P<video_id>\d+)$', views.play, name='play'),
    url(r'^play/(?P<video_id>\d+)$', views.play, name='play'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'offtube/login.html'}, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
)
