from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from memorix.settings import EMAIL_HOST_USER
from .models import Album
from django.core.mail import send_mail

def send_emails_view(request, album_id):
    if request.method == 'POST':
        album = Album.objects.get(id=album_id)
        recipient_list = [e.email for e in album.emails.all()]
        
        if not recipient_list:
            messages.warning(request, "No email addresses associated with this album.")
            return redirect("admin:albums_album_change", album_id)
        
        link = request.build_absolute_uri(album.get_absolute_url())

        send_mail(
            subject="Your Memorix Album",
            message=f"Here is your link to your album: {link}",
            from_email=EMAIL_HOST_USER,
            recipient_list=recipient_list,
        )
        messages.success(request, "Emails sent successfully.")
        return redirect("admin:albums_album_change", album_id)


def album_view(request, share_token):
    album = get_object_or_404(Album, share_token=share_token)
    photos = album.photos.all()
    
    context = {
        'album': album,
        'photos': photos,
    }
    return render(request, 'albums/album_view.html', context)