# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from django_zotero import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<doc_id>\d+)/$', views.detail, name='detail'),
)
