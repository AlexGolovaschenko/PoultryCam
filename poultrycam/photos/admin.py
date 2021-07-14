from django.contrib import admin

from .models import Photo, PhotoMetaData


class PhotoMetaDataInline (admin.StackedInline):
	model = PhotoMetaData


class PhotoAdmin (admin.ModelAdmin):
	list_display = ['__str__', 'upload_date', 'marker']
	inlines = [PhotoMetaDataInline]


admin.site.register(Photo, PhotoAdmin)
