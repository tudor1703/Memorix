from django.contrib import admin
from .models import Album, AlbumPhoto, AlbumEmail

class AlbumPhotoInline(admin.TabularInline):
    model = AlbumPhoto
    extra = 1
    readonly_fields = ("uploaded_at",)

class AlbumEmailInline(admin.TabularInline):
    model = Album.emails.through
    extra = 1

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at", "photo_count", "participant_count")
    search_fields = ("title", "user__email")
    inlines = [AlbumPhotoInline, AlbumEmailInline]
    exclude = ("emails",)

    readonly_fields = ("share_token",)

    @admin.display(description="Photos")
    def photo_count(self, obj):
        return obj.photos.count()

    @admin.display(description="PhoParticipantstos")
    def participant_count(self, obj):
        return obj.emails.count()

    actions = ["delete_selected_albums"]

    @admin.action(description="Delete selected albums")
    def delete_selected_albums(self, request, queryset):
        queryset.delete()

@admin.register(AlbumPhoto)
class AlbumPhotoAdmin(admin.ModelAdmin):
    list_display = ("album", "caption", "uploaded_at")

@admin.register(AlbumEmail)
class AlbumEmailAdmin(admin.ModelAdmin):
    list_display = ("email",)
