# -*- coding: utf-8 -*-
from django.views.generic.list_detail import object_detail
from django.shortcuts import render_to_response
from django.template import RequestContext
from gallery.models import Gallery, GalleryPhoto

def indirect(request, ctype, oid):
    """ For reversing based on a ctype & object id in templates """
    gallery = Gallery.live.get(content_type__pk=ctype, object_id=oid)
    return render_to_response('gallery/standalone.html', {'object': gallery},
        context_instance=RequestContext(request))
    
def photo_detail(request, gallery_slug, object_id):
    """ Wrapper for object_detail on GalleryPhoto to work with giving a dummy slug """
    return object_detail(request, GalleryPhoto.objects.all(), object_id=object_id)

def photo_list(request):
   return render_to_response('gallery/gallery_list.html', {'object': GalleryPhoto.objects.all().order_by('gallery')},
        context_instance=RequestContext(request))
   
def overview(request):
    """  """
    galleries = Gallery.objects.all() 
       
    return render_to_response('gallery/gallery_overview.html', {'object': galleries},
        context_instance=RequestContext(request))
    
   
