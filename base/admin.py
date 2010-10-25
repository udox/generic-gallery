from django.contrib import admin

class BaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', )
    ordering = ('-created_at',)

    save_on_top = True

    fieldsets = (
        (None, { 'fields' : ('name', 'status', 'created_at',) }),
        ('URL Information', { 'fields' : ('slug',), 'classes' : ['collapsed',] }),
    )

    prepopulated_fields = { 'slug' : ('name',) }

    def save_model(self, request, obj, form, change):
        """Checks whether our model has a user field and if so assigns it
        to the requested user. Should probably go in Ownable admin but stacking
        all these things together to inherit off of is a bit messy """

        if hasattr(obj, 'user'):
            obj.user = request.user
        super(BaseAdmin, self).save_model(request, obj, form, change)


#Fieldsets are defined for the abstact class models. Then
#in your concrete modelAdmins import the admin's below and
#concatenate __CLASS__.fieldsets to your modelAdmin fieldset

class PostAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Content', { 'fields' : ('body',)}),
    )

class LocationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Location & Mapping', { 'fields' : (
            'location_name',
            'latitude_longitude',
            #'display_address', # disable this for now
            'address_1',
            'address_2',
            'city',
            'zipcode',
            'state',
            'country',
        )}),
    )

class DateBracketAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Date & Time', { 'fields' : (('start_date', 'start_time'), ('end_date', 'end_time'))}),
    )

class ImageBodyAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Media', { 'fields' : ('main_image',)}),
    )

class OwnerAdmin(admin.ModelAdmin):
    fieldsets = (
        ('User Assignment', { 'fields' : ('user',)}),
    )

class TagAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Tags', { 'fields' : ('tags',)}),
    )



