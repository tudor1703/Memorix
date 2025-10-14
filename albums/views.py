from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Album


def send_emails_view(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    recipients = [e.email for e in album.emails.all()]
    full_url = request.build_absolute_uri(album.get_absolute_url())

    messages.success(
        request,
        f"Simulated: emails marked as sent to {len(recipients)} participant(s)."
    )

    change_url = reverse("admin:albums_album_change", args=[album_id])
    return redirect(f"{change_url}?emails_sent=1")


def album_view(request, share_token):
    album = get_object_or_404(Album, share_token=share_token)
    photos = album.photos.all()
    
    context = {
        'album': album,
        'photos': photos,
    }
    return render(request, 'albums/album_view.html', context)