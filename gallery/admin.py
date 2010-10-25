# -*- coding: utf-8 -*-
from gallery.models import Gallery, GalleryPhoto, BulkUpload
from django.contrib.contenttypes.models import ContentType
from base.admin import *
from base.templatetags.custom_filters import live_thumbnail
from django import forms
from django.contrib import admin
from datetime import datetime
from gallery.bulkupload import bulkupload

# nicked from: http://www.djangosnippets.org/snippets/934/
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.conf import settings
from PIL import Image
import os

def thumbnail(image_path):
    absolute_url = '/media/'+image_path
    return u'<img src="%s" alt="%s" style="width:250px;" />' % (absolute_url, image_path)

class AdminImageWidget(AdminFileWidget):
    """
    A FileField Widget that displays an image instead of a file path
    if the current file is an image.
    """
    def render(self, name, value, attrs=None):
        output = []
        file_name = str(value)
        if file_name:
            file_path = '%s%s' % (settings.MEDIA_URL, file_name)
            try:            # is image
                Image.open(os.path.join(settings.MEDIA_ROOT, file_name))
                output.append('<a target="_blank" href="%s">%s</a><br />%s <a target="_blank" href="%s">%s</a><br />%s ' % \
                    (file_path, thumbnail(file_name), _('Currently:'), file_path, file_name, _('Change:')))
            except IOError: # not image
                output.append('%s <a target="_blank" href="%s">%s</a> <br />%s ' % \
                    (_('Currently:'), file_path, file_name, _('Change:')))
        #print output
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
# end theft - TODO: refactor into widget file - working on shell atm ~jaymz

class BulkUploadForm(forms.ModelForm):
    
    class Meta:
        model = BulkUpload
        exclude = ('process', 'processing_time',)

class GalleryPhotoAdminForm(forms.ModelForm):
    main_image = forms.ImageField(widget=AdminImageWidget)

    class Meta:
        model = GalleryPhoto


class GalleryForm(forms.ModelForm):
    model = Gallery

    class Media:
        js = (
            '/media/js/jquery-1.3.2.min.js',
            '/media/js/jquery-ui-1.7.2.custom.min.js',
            '/media/js/admin_sortables.js',
        )

class GalleryPhotoAdmin(admin.TabularInline):
    model = GalleryPhoto
    form = GalleryPhotoAdminForm
    extra = 5
    allow_add = True

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'content_type', 'object_id', 'count')
    list_filter = ('status', 'content_type')
    inlines = [GalleryPhotoAdmin,]
    form = GalleryForm

    fieldsets = (
        ('Associated Content', { 'fields' : ('content_type', 'object_id')}),
        ('Size & Format', { 'fields' : (('thumbnail_size', 'render_size'), 'display_using')}),
    )
    fieldsets = BaseAdmin.fieldsets + fieldsets

    def save_model(self, request, obj, form, change):
        #print "save model called"
        if request.POST.get('content_type'):
            try:
                ctype = ContentType.objects.get(pk=request.POST.get('content_type'))
                self.content_type = ctype
            except:
                pass
        #super(GalleryAdmin, self).save_model(self, request, obj, form, change)
        obj.save()


class BulkUploadAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields' : ('job_name', 'zipfile', 'gallery' )}),
        ('Debug Report', { 'fields' : ('report',), 'classes' : ['collapse',]}),
    )
    list_display = ('job_name', 'date_added', 'zipfile', 'process', 'processing_time','gallery')
    list_editable = ('process',)
    model = BulkUpload
    form = BulkUploadForm

    def save_model(self, request, obj, form, change):
        if obj.processing_time == None and obj.process == False:
            obj.save() # save it the first time on creation
        elif obj.processing_time == None and obj.process == True:
            #obj.report = bulkupload(obj.zipfile) # call bulk upload on it
            obj.report = bulkupload(obj) # call bulk upload on it
            obj.processing_time = datetime.now()
            obj.save()
        else:
            pass # do nothing


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(GalleryPhoto)
admin.site.register(BulkUpload, BulkUploadAdmin)
