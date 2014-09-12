# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from django_zotero import views

urlpatterns = patterns('',
    url(r'^itemtypes/valid/$',
        views.valid_zotero_itemtypes_fields,
        name='valid_zotero_itemtypes_fields'),
    url(r'^itemtype/fields/$',
        views.itemtype_fields_view,
        name='zotero_itemtype_fields'),
    
    url(r'^$', views.index, name='index'),
    url(r'^(?P<doc_id>\d+)/$', views.detail, name='detail'),
)
