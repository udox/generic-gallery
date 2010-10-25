# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns
from gallery.models import Gallery, GalleryPhoto


urlpatterns = patterns('',
    (r'^thumbnail-view/(?P<object_id>[\d]+)', 'django.views.generic.list_detail.object_detail', {
        'template_name': 'gallery/standalone.html',
        'queryset' : Gallery.live.all()
    }, 'direct_pk'),
    (r'^(?P<gallery_slug>[\w-]+)/(?P<object_id>\d+)/$', 'gallery.views.photo_detail', {}, 'photo_detail'),
    
    (r'^standalone/(?P<ctype>\d+)/(?P<oid>\d+)/$', 'gallery.views.indirect', {}, 'indirect'),
    
    (r'^(?P<slug>[\w-]+)', 'django.views.generic.list_detail.object_detail', {
        'slug_field': 'slug',
        'template_name': 'gallery/standalone.html',
        'queryset' : Gallery.live.all()
    }, 'direct_slug'),    
)
#TODO: check if (r'^(?P<slug>[\w-]+)', is being used