from django.db import models

class Album(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class AlbumEmail(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    albums = models.ManyToManyField(Album, related_name="emails")

    def __str__(self):
        return self.subject


class AlbumPhoto(models.Model):
    photo = models.ImageField(upload_to="album_photos/")
    caption = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="photos")

    def __str__(self):
        return f"Photo in {self.album.title}"
