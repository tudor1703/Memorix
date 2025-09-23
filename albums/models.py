from django.db import models
from django.conf import settings
import uuid

class Album(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    share_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,     
        related_name="albums"     
    )
    def __str__(self):
        return self.title


class AlbumEmail(models.Model):
    album = models.ForeignKey(
        "Album", on_delete=models.CASCADE, related_name="album_emails"
        )
    email = models.EmailField() 

    def __str__(self):
        return f"{self.email} (Album: {self.album.title})"


class AlbumPhoto(models.Model):
    photo = models.ImageField(upload_to="album_photos/")
    caption = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="photos")

    def __str__(self):
        return f"Photo in {self.album.title}"
