from django.db import models
#from base.models import NoPostBase
from sorl.thumbnail.fields import ImageWithThumbnailsField
from django.template.defaultfilters import slugify, lower
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def get_image_path(instance, filename):
    return 'galleries/%s/%s' % (slugify(instance.gallery.name), filename)

class Gallery(NoPostBase):
    CREATED_VIA_CHOICES = (
        (0, 'Made via django admin'),
        (1, 'Auto-made via ZIP'),
    )
    
    STATUS_CHOICES = (
        (0, 'Offline'),
        (3, 'Preview'),
        (5, 'Live'),
    )
    name = models.CharField(max_length=255)
    slug = SlugNullField(null=True, blank=True, unique=True, max_length=255)
    slug.help_text = 'Used to complete the url to create a unique link'
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=5)
    status.help_text = 'Use this to take items off the site without deleting them'    
    
    created_via = models.IntegerField(choices=CREATED_VIA_CHOICES, editable=False, default=0)
    thumbnail_size = models.CharField(max_length=20, choices=settings.GALLERY['THUMBNAIL_SIZES'])
    render_size = models.CharField(max_length=20, choices=settings.GALLERY['RENDER_SIZES'])
    display_using = models.CharField(max_length=1, choices=settings.GALLERY['DISPLAY_OPTIONS'])

    content_type = models.ForeignKey(ContentType, blank=True, null=True) #default to news
    content_type.help_text = 'What type of content to link this to. Typically you will want to use news which is the default.'
    object_id = models.PositiveIntegerField(blank=True, null=True)
    object_id.help_text = 'This is the object id, you can see this in the permalink or the <em>id</em> column in the admin for the news and reviews.'
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    tags = TagField(blank=True, null=True)
   
    objects = models.Manager()
    live = LiveManager()
    
    def get_tags(self):
        return Tag.objects.get_for_object(self)

    @property
    def count(self):
        return (GalleryPhoto.objects.filter(gallery=self.id)).count()

    def __unicode__(self):
        return '%s - %d Photos' % (self.name, self.count)

    def photos(self):
        return GalleryPhoto.objects.filter(gallery=self.id)
    
    @property    
    def pk_list(self):
      return list(self.galleryphoto_set.all().values_list('pk', flat=True))
  
    @models.permalink
    def get_absolute_url(self):
        return ('gallery:direct_pk', (), {'object_id': self.pk,})

class GalleryPhoto(models.Model):
    order = models.IntegerField(blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length=100)
    gallery = models.ForeignKey(Gallery, blank=True, null=True)

    main_image = ImageWithThumbnailsField(
        upload_to=get_image_path,
        null=True,
        blank=True,
        thumbnail = {'size' : (100, 100)},
        extra_thumbnails = settings.GALLERY['ET_DEFINITIONS'],
    )

    def __unicode__(self):
        return '%s' % self.main_image

    class Meta:
        ordering = ('order',)
    
    @models.permalink
    def get_absolute_url(self):
        return ('gallery:photo_detail', (), {'object_id': self.pk, 'gallery_slug': slugify(self.gallery.name)})
   
    def next(self):
        return self.photo_at_index(offset=1)

    def previous(self):
        return self.photo_at_index(offset=-1)
    
    def photo_at_index(self, offset):
        """ Returns the next photo in the gallery set from this one """       
        photo_index = self.gallery_postition + offset       
        pk_list = self.gallery.pk_list
        if photo_index == len(pk_list):
            photo_pk = pk_list[0]
        else:
            photo_pk = pk_list[photo_index]       
        return GalleryPhoto.objects.get(pk=photo_pk)  
    
    @property
    def gallery_postition(self):
        """ Returns the position in the gallery list (index) for this photo """
        return self.gallery.pk_list.index(self.pk)       
    
fs = FileSystemStorage(location=settings.GALLERY['BULK_PATH'])

class BulkUpload(models.Model):
    job_name = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    zipfile = models.FileField(upload_to='bulkuploads', storage=fs)
    process = models.BooleanField(default=False)
    processing_time = models.DateTimeField(blank=True, null=True)
    report = models.TextField(blank=True, null=True)
    gallery = models.ForeignKey(Gallery, blank=True, null=True)

    class Meta:
        verbose_name = 'Bulk uploads'
        verbose_name_plural = 'Bulk uploads'
