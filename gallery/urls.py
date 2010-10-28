# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns
from gallery.models import Gallery, GalleryPhoto


urlpatterns = patterns('',
                       
    (r'^slide/(?P<gallery_id>[\d]+)/$', 'django.views.generic.simple.direct_to_template', {
        'template' : 'gallery/slide.html',
        'extra_context' : {
            'gallery' : Gallery.objects.all(),
        }
    }),                   
                       
    (r'^photo/(?P<object_id>[\d]+)', 'django.views.generic.list_detail.object_detail', {
        'template_name': 'gallery/gallery_photo.html',
        'queryset': GalleryPhoto.objects.all()
    }, 'photo_pk'),
                      
    (r'^g/page(?P<page>[0-9]+)/$', 'django.views.generic.list_detail.object_detail', {        
        'paginate_by': 2,                                                                
        'template_name': 'gallery/gallery_pagi.html',
        'queryset' : Gallery.live.all()
    }, 'grid'),
    
    (r'^grid/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', {                                                                
        'template_name': 'gallery/gallery_list.html',
        'queryset' : Gallery.live.all()
    }, 'grid_pk'),
    
#    (r'^all/(?P<slug>[\w-]+)/(?P<object_id>[\d]+)', 'django.views.generic.list_detail.object_detail', {
#        'slug_field': 'slug',
#        'template_name': 'gallery/standalone.html',
#        'queryset': Gallery.live.all()
#    }, 'direct_slug'),     
    (r'^thumbnail-view/(?P<object_id>[\d]+)', 'django.views.generic.list_detail.object_detail', {
        'template_name': 'gallery/standalone.html',
        'queryset': Gallery.live.all()
    }, 'direct_pk'),
    (r'^(?P<gallery_slug>[\w-]+)/(?P<object_id>\d+)/$', 'gallery.views.photo_detail', {}, 'photo_detail'),
    
    (r'^standalone/(?P<ctype>\d+)/(?P<oid>\d+)/$', 'gallery.views.indirect', {}, 'indirect'),
    
   
)
#TODO: check if (r'^(?P<slug>[\w-]+)', is being used