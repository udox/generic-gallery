# -*- coding: utf-8 -*-
from django.views.generic.list_detail import object_detail
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from gallery.models import Gallery, GalleryPhoto
from django.conf import settings

def indirect(request, ctype, oid):
    """ For reversing based on a ctype & object id in templates """
    gallery = Gallery.live.get(content_type__pk=ctype, object_id=oid)
    return render_to_response('gallery/standalone.html', {'object': gallery},
        context_instance=RequestContext(request))
    
def photo_detail(request, gallery_slug, object_id):
    """ Wrapper for object_detail on GalleryPhoto to work with giving a dummy slug """
    return object_detail(request, GalleryPhoto.objects.all(), object_id=object_id)

def grid_detail(request, gallery_slug, object_id):
    """  """
    try:
        gallery = Gallery.objects.get(id=object_id)        
    except:
        raise Http404 
    slug = slugify(gallery.name)
        
    return render_to_response('gallery/gallery_grid.html', {'object': gallery },
        context_instance=RequestContext(request))

def photo_list(request):
    return render_to_response('gallery/gallery_list.html', {'object': GalleryPhoto.objects.all().order_by('gallery')},
        context_instance=RequestContext(request))
   
def overview(request):
    """  """
    galleries = Gallery.objects.all() 
    pics = GalleryPhoto.objects.all()    
    return render_to_response('gallery/gallery_overview.html', {'object': galleries, 'pics': pics,},
        context_instance=RequestContext(request))
    
def ajax(request):
    """ 
    Deals with jquery ajax call for inline gallery /ajax
    """
    #TODO add try catches
    if request.is_ajax():
        if request.method == 'GET':
            message = "GET"
        elif request.method == 'POST':
            img = GalleryPhoto.objects.get(id=request.POST['img'])           
            message = "%s%s" % (settings.MEDIA_URL, img.main_image.extra_thumbnails['mainbody'].relative_url)
            
    else:
        message = "ajax fail"
    return HttpResponse(message)
    
   
