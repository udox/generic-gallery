# -*- coding: utf-8 -*-
from zipfile import ZipFile
import tempfile
import os
from glob import glob
from string import Template
from datetime import datetime
from django.core.files import File
from gallery.models import Gallery, GalleryPhoto


def bulkupload(obj):
    """ TODO: refactor function to be generic, not CTproduct related """
    z = ZipFile(obj.zipfile) # this will be the file field of our model on save
    upload_prefix = 'uploads/galleries/'
    target = tempfile.mkdtemp()
    z.extractall(target)
    folders = os.listdir(target)
    report = ""
    for folder in folders:
        if folder is not '__MACOSX':
            images = [image for image in os.listdir(os.path.join(target, folder))]
            images.sort()
            if not obj.gallery:
                obj_gallery = Gallery.objects.create(name=folder)                
                obj_gallery.created_via = 1
                obj_gallery.save()
                report += "Added new gallery for %s - gallery pk = %d\n" % (folder, obj_gallery.pk)
            else:
                report += "Adding images to existing gallery pk = %d\n" % (obj.gallery.pk)
            cnt = 1
            for image in images:
                if ".jpg" in image or ".png" in image or ".gif" in image or ".jpeg" in image:
                    f = File(open(os.path.join(target, folder, image), 'r'))
                    if obj.gallery:
                        obj_gallery = obj.gallery
                    gallery_image = GalleryPhoto.objects.create(gallery=obj_gallery, main_image=f)
                    gallery_image.save()
                    gallery_image.main_image.save(image, f)
                    report += "Added gallery image - pk = %d\n" % gallery_image.pk
                    cnt += 1
    return str(report)
