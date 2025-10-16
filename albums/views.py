from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from memorix.settings import EMAIL_HOST_USER
from .models import Album
from django.http import HttpResponse
from django.core.mail import send_mail


def send_emails_view(request, album_id):
    if request.method == 'POST':
        album = Album.objects.get(id=album_id)
        send_mail(
            subject="Test Email",
            message="This is a test email from Memorix.",
            from_email=EMAIL_HOST_USER,
            recipient_list=["mircatudor06@gmail.com"],
        )
        return HttpResponse("Email sent successfully!")
    return render(request, "albums/send_email.html")

def album_view(request, share_token):
    album = get_object_or_404(Album, share_token=share_token)
    photos = album.photos.all()
    
    context = {
        'album': album,
        'photos': photos,
    }
    return render(request, 'albums/album_view.html', context)