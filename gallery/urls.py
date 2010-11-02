# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns
from gallery.models import Gallery, GalleryPhoto


urlpatterns = patterns('',
    (r'^overview/$', 'gallery.views.overview', {}, 'overview'),
            
    (r'^slider/(?P<gallery_id>[\d]+)/$', 'django.views.generic.simple.direct_to_template', {
        'template' : 'gallery/gallery_slider.html',
        'extra_context' : {
            'gallery' : Gallery.objects.all(),
        }
    }),                   
                       
    (r'^photo/(?P<slug>[\w-]+)/(?P<object_id>[\d]+)', 'django.views.generic.list_detail.object_detail', {
        'slug_field': 'slug',
        'template_name': 'gallery/gallery_photo.html',
        'queryset': GalleryPhoto.objects.all()
    }, 'photo_pk'),
                      
    (r'^g/page(?P<page>[0-9]+)/$', 'django.views.generic.list_detail.object_detail', {        
        'paginate_by': 2,                                                                
        'template_name': 'gallery/gallery_pagi.html',
        'queryset' : Gallery.live.all()
    }, 'grid'),
    
    (r'^grid/(?P<gallery_slug>[\w-]+)/(?P<object_id>\d+)/$', 'gallery.views.grid_detail', {}, 'grid_detail'),
    
#    (r'^grid/(?P<gallery_slug>[\w-]+)/(?P<object_id>\d+)/$', 'django.views.generic.simple.direct_to_template', {
#        'template' : 'gallery/gallery_grid.html',
#        'extra_context' : {
#            'object' : Gallery.live.all(),
#            
#        }
#    },'grid_detail'), 
    
#    (r'^grid/[\w-]+/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', { 
#        #'slug': 'gallery_slug',       
#        'template_name': 'gallery/gallery_list.html',
#        'queryset' : Gallery.live.all()
#    }, 'grid_pk'),
       
    (r'^thumbnail-view/(?P<object_id>[\d]+)', 'django.views.generic.list_detail.object_detail', {
        'template_name': 'gallery/standalone.html',
        'queryset': Gallery.live.all()
    }, 'direct_pk'),
    
    (r'^(?P<gallery_slug>[\w-]+)/(?P<object_id>\d+)/$', 'gallery.views.photo_detail', {}, 'photo_detail'),
    
    (r'^standalone/(?P<ctype>\d+)/(?P<oid>\d+)/$', 'gallery.views.indirect', {}, 'indirect'),    
   
)