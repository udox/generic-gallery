from django.template import Library
from django.db.models import loading
from django.contrib.contenttypes.models import ContentType
from gallery.models import Gallery, GalleryPhoto
from settings import MEDIA_URL, GALLERY

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
            'gallery': gallery.name,
            'pic_total': pic_total,
            'created': gallery.created_at,
    }
    
    
@register.inclusion_tag('gallery/tags/gallery_totals_tag.html')
def gallery_totals(galleries, pics):
    """ Simple stats for all galleries """
    gallery_total = galleries.count()
    pics_total = pics.count() 
    return {
            'gallery_total': gallery_total,
            'pics_total': pics_total,            
    }