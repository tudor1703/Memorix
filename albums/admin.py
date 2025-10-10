from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline


from .models import Album, AlbumPhoto, AlbumEmail
from .views import send_emails_view

class AlbumPhotoInline(TabularInline):
    model = AlbumPhoto
    extra = 1
    readonly_fields = ("uploaded_at",)

class AlbumEmailInline(TabularInline):
    model = Album.emails.through
    extra = 1

@admin.register(Album)
class AlbumAdmin(ModelAdmin):
    list_display = ("title", "user", "created_at", "photo_count", "participant_count")
    search_fields = ("title", "user__email")
    inlines = [AlbumPhotoInline, AlbumEmailInline]
    exclude = ("emails",)

    readonly_fields = ("share_token",)

    @admin.display(description="Photos")
    def photo_count(self, obj):
        return obj.photos.count()

    @admin.display(description="Participants")
    def participant_count(self, obj):
        return obj.emails.count()

    actions = ["delete_selected_albums"]

    @admin.action(description="Delete selected albums")
    def delete_selected_albums(self, request, queryset):
        queryset.delete()
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:album_id>/send_emails/',
                 self.admin_site.admin_view(send_emails_view),
                 name='albums_album_send_emails'),
        ]
        return custom_urls + urls

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        send_url = reverse('admin:albums_album_send_emails', args=[object_id])
        extra_context['send_emails_button'] = format_html(
            '<a class="button" href="{}">Send Emails</a>', send_url
        )
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

@admin.register(AlbumPhoto)
class AlbumPhotoAdmin(admin.ModelAdmin):
    list_display = ("album", "caption", "uploaded_at")

@admin.register(AlbumEmail)
class AlbumEmailAdmin(admin.ModelAdmin):
    list_display = ("email",)
