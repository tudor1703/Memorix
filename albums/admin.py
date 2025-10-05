from django.contrib import admin
from .models import Album, AlbumPhoto, AlbumEmail

# Inline pentru fotografii
class AlbumPhotoInline(admin.TabularInline):
    model = AlbumPhoto
    extra = 1
    readonly_fields = ("uploaded_at",)

# Inline pentru participanți (email)
class AlbumEmailInline(admin.TabularInline):
    model = Album.emails.through
    extra = 1

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at", "photo_count", "participant_count")
    search_fields = ("title", "user__email")
    inlines = [AlbumPhotoInline, AlbumEmailInline]

    readonly_fields = ("share_token",)

    # Statistici
    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.short_description = "Photos"

    def participant_count(self, obj):
        return obj.emails.count()
    participant_count.short_description = "Participants"

    # Delete albums direct din listă
    actions = ["delete_selected_albums"]

    @admin.action(description="Șterge albumele selectate")
    def delete_selected_albums(self, request, queryset):
        queryset.delete()

@admin.register(AlbumPhoto)
class AlbumPhotoAdmin(admin.ModelAdmin):
    list_display = ("album", "caption", "uploaded_at")

@admin.register(AlbumEmail)
class AlbumEmailAdmin(admin.ModelAdmin):
    list_display = ("email",)
