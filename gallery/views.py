# -*- coding: utf-8 -*-
from django.views.generic.list_detail import object_detail
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from gallery.models import Gallery, GalleryPhoto
from django.conf import settings
from django.utils import simplejson
from django.core import serializers
from time import time
import os

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
 
def download(request, image_id):
    """ uses id from url and then serves image """
    photo = GalleryPhoto.objects.get(id=image_id)#.main_image
    url = photo.main_image
    response = HttpResponse(url, mimetype='image/jpeg', )
    filename = "attachment; filename=%s" % os.path.basename(photo.main_image.name)
    response['Content-Disposition'] = filename
    return response

def ajax(request):
    """ 
    Deals with jquery ajax call for inline gallery /ajax
    TODO:
        404 if photo ID isn't found in db?
        add image name to tag
    """    
    data = {}   
    if request.is_ajax():
        if request.method == 'GET':
            pass
        if request.method == 'POST':
            try: 
                img = GalleryPhoto.objects.get(id=request.POST['img'])
            except:
                pass
            url = "%s%s" % (settings.MEDIA_URL, img.main_image.extra_thumbnails['mainbody'].relative_url)            
            dimensions = "%sx%s" % (img.main_image.width, img.main_image.height)
            if img.name:
                name = img.name
            else:
                name = None          
            data = {              
                'main_gallery': img.gallery.name,               
                'main_url': url,
                'main_name': name,        
                'orig_size': img.main_image.size/1024,
                'orig_id': img.id, 
                'orig_dimension': dimensions,
                'orig_url': img.main_image.url,
                'orig_name': os.path.basename(img.main_image.name)       
            }                       
    else:
        pass
    return render_to_response('gallery/tags/gallery_image_stats_tag.html', {'data': data, },
        context_instance=RequestContext(request))