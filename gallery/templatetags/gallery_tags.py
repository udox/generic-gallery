from django.template import Library
from django.db.models import loading
from django.contrib.contenttypes.models import ContentType
from gallery.models import Gallery, GalleryPhoto
from settings import MEDIA_URL, GALLERY, CONTENT_LIMITS
import random

register = Library()

# TODO: most of these tags have actual required fields, the none is probably to
# bypass it on dodgy data whilst building... remove/force at end.

@register.inclusion_tag('gallery/gallery_output.html')
def display_gallery(app_name=None, model_name=None, oid=None, show_thumbs=True):
    """
        render out a gallery for a particular object. in the template
        you can use '0' to cause it to render with links rather than
        thumbnails. eg:

        {% display_gallery "news" object.id 0 %}

    """
    images = []
    # load our model up, this loads APP/MODEL so News.News, Review.Review etc will
    # work fine for it, then grab the gallery images for this and render with template
    try:
        model = loading.get_model(app_name, model_name)
        ctype = ContentType.objects.get_for_model(model)
        g = Gallery.live.get(content_type=ctype, object_id=oid)
        images = GalleryPhoto.objects.all().filter(gallery=g)
    except:
        pass
    data = {
        'gallery_images' : images,
        'MEDIA_URL' : MEDIA_URL,
        'show_thumbs' : show_thumbs,
        'contenttype' : model_name,
    }
    return data

@register.simple_tag
def display_gallery_link(app_name=None, model_name=None, oid=None, link_text='Open Gallery'):
    """
        writes out a link for the gallery for a particular id, you can override the
        text with the third argument
    """
    try:
        model = loading.get_model(app_name, model_name)
        ctype = ContentType.objects.get_for_model(model)
        g = Gallery.live.get(content_type=ctype, object_id=oid)
        return '<a class="iframe-gallery" href="/gallery/%d/?iframe">%s</a>' % (g.id, link_text)
    except:
        return ''

def has_gallery(model_name=None, oid=None):
    try:
        model = loading.get_model(model_name, model_name)
        ctype = ContentType.objects.get_for_model(model)
        g = Gallery.live.get(content_type=ctype, object_id=oid)
        if g:
            return True
        else:
            return False
    except:
        return False

@register.inclusion_tag('gallery/gallery_list.html')
def gallery_list():
    photos = GalleryPhoto.objects.all()
    return photos

@register.inclusion_tag('gallery/gallery_grid.html')
def gallery_grid(app_name, model_name, oid, limit=GALLERY['GRID_LIMIT']):
    data = dict(pics=None)
    try:
        model = loading.get_model(app_name, model_name)
        ctype = ContentType.objects.get_for_model(model)
        # We might have more than 1 gallery returned
        g = list(Gallery.live.filter(content_type=ctype, object_id=oid))[-1]
        _pics = g.photos().all()[:limit]
        data = dict(pics=_pics, content_type=ctype.pk, pk=oid)
    except IndexError:
        pass
    return data

@register.inclusion_tag('gallery/gallery_grid.html')
def gallery_as_grid(gallery, limit=GALLERY['GRID_LIMIT']):
    first_pic = gallery.photos().all()[0]
    return dict(pics=gallery.photos().all()[:limit], first_pic=first_pic)

@register.inclusion_tag('gallery/inline-slideshow.html')
def gallery_gallery(gallery_id):
    """
    The parameter passed for this method is sent by the gallery.url
    """
    gallery = None
    try:
        gallery = Gallery.objects.get(id=gallery_id)
    except:
        pass
    return {
        'gallery' : gallery,
    }
    
@register.inclusion_tag('gallery/tags/gallery_stats_tag.html')
def gallery_stats(gallery):
    """ Simple stats for gallery object param """
    pic_total = gallery.photos().count()   
    return {
            'gallery': gallery,
            'pic_total': pic_total,          
    }    
    
@register.inclusion_tag('gallery/tags/gallery_totals_tag.html')
def gallery_totals(galleries, pics, latest_created=None):
    """ 
    Simple total stats for all galleries 3rd para is boolean to show extra info
    regarding latest gallery created    
    """    
    gallery_total = galleries.count()
    pics_total = pics.count() 
    if latest_created:
        latest_created = Gallery.objects.all().order_by('-created_at')[:1][0].created_at
    return {
            'gallery_total': gallery_total,
            'pics_total': pics_total, 
            'latest_created': latest_created,           
    }    

@register.inclusion_tag('gallery/tags/gallery_random_pic_tag.html')
def gallery_random(info=None):
    """ Grab random image from photos info boolean to add gallery_stats tag in template tag """
    pics = GalleryPhoto.objects.all()
    random_pic = pics[random.randint(0,pics.count()-1)]   
    return {
        'random_pic' : random_pic,
        'info': info,
    }
    
@register.inclusion_tag('gallery/tags/gallery_first_last_tag.html')
def gallery_first_last(gallery, image=None):
    """ 
    expects a gallery object then outputs first or last image of gallery dependant
    on params defaults to first
    
    """
    if image == 'last':
        pic = gallery.photos()[0]    
    else:
        pic = gallery.photos()[gallery.photos().count()-1]
    return {
        'pic' : pic,
    }
    
@register.inclusion_tag('gallery/tags/gallery_pagination_tag.html')
def render_pagination(page, paginator):
    """ Returns a paginator which always puts the current page in the
    center of the page links to show, unless its near the start or
    end in which case it is dropped in as normal. """
       
    items = CONTENT_LIMITS['PAGINATION']
    half = int(items/2) 

    start = page  

    end = page + items 

    if page > half: 
        start -= half
        end -= half
    else:
        start = 1
        end = items

    if end > paginator.num_pages:
        end = paginator.num_pages
        start = end - items

    if start < 0:
        start = 1
        end = CONTENT_LIMITS['PAGINATION']
        
    if start > 1:
        last_page = True
    else:
        last_page = False
     
#    if page_range > end:
#        page_range = page_range[page_range]
    page_range = range(start, end)
    #page_range = page_range[page_range]   
    
    return {
        'page' : page,
        'page_range': page_range,
        'last_page': last_page,
    }
    