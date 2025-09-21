from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PhotoAlbum(models.Model):
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Photo {self.id}"


class Album(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    photos = models.ManyToManyField(PhotoAlbum, related_name='albums')  # many-to-many
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class EmailAlbum(models.Model):
    email = models.EmailField()
    albums = models.ManyToManyField(Album, related_name='email_albums')  # many-to-many
    shared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
