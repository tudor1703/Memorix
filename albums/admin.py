from django.contrib import admin
from .models import Album, AlbumPhoto, AlbumEmail

admin.site.register(Album)
admin.site.register(AlbumPhoto)
admin.site.register(AlbumEmail)
