from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html

from .models import Album, AlbumPhoto, AlbumEmail
from .views import send_emails_view

class AlbumPhotoInline(admin.TabularInline):
    model = AlbumPhoto
    extra = 1
    readonly_fields = ("uploaded_at",)

class AlbumEmailInline(admin.TabularInline):
    model = Album.emails.through
    extra = 1

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at", "photo_count", "participant_count", "view_album_link")
    search_fields = ("title", "user__email")
    inlines = [AlbumPhotoInline, AlbumEmailInline]
    exclude = ("emails",)

    readonly_fields = ("view_album_link",)

    @admin.display(description="Photos")
    def photo_count(self, obj):
        return obj.photos.count()

    @admin.display(description="Participants")
    def participant_count(self, obj):
        return obj.emails.count()

    @admin.display(description="Album URL")
    def view_album_link(self, obj):
        if obj.id:
            from django.contrib.sites.shortcuts import get_current_site
            from django.http import HttpRequest
            
            # Create a mock request to get the current site
            request = HttpRequest()
            request.META['HTTP_HOST'] = '127.0.0.1:8000'  # For development
            request.META['wsgi.url_scheme'] = 'http'
            
            url = reverse('albums:album_view', args=[obj.id])
            full_url = f"http://127.0.0.1:8000{url}"
            return format_html('<a href="{}">{}</a>', full_url, full_url)
        return "-"

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
        view_url = reverse('albums:album_view', args=[object_id])
        extra_context['send_emails_button'] = format_html(
            '<a class="button" href="{}">Send Emails</a>', send_url
        )
        extra_context['view_album_button'] = format_html(
            '<a class="button" href="{}">View Album</a>', view_url
        )
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

@admin.register(AlbumPhoto)
class AlbumPhotoAdmin(admin.ModelAdmin):
    list_display = ("album", "caption", "uploaded_at")

@admin.register(AlbumEmail)
class AlbumEmailAdmin(admin.ModelAdmin):
    list_display = ("email",)
