from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from memorix.settings import EMAIL_HOST_USER
from .models import Album
from django.http import HttpResponseRedirect, JsonResponse
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect
from django.http import JsonResponse

def send_emails_view(request, album_id):
    if request.method == 'POST':
        album = Album.objects.get(id=album_id)
        recipient_list = [e.email for e in album.emails.all()]
        
        if not recipient_list:
            return JsonResponse({'message': 'No recipients found. Email not sent.'})
        
        link = request.build_absolute_uri(album.get_absolute_url())

        send_mail(
            subject="Your Memorix Album",
            message=f"Here is your link to your album: {link}",
            from_email=EMAIL_HOST_USER,
            recipient_list=recipient_list,
        )
        return JsonResponse({'message': 'Email sent successfully!'})
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)


def album_view(request, share_token):
    album = get_object_or_404(Album, share_token=share_token)
    photos = album.photos.all()
    
    context = {
        'album': album,
        'photos': photos,
    }
    return render(request, 'albums/album_view.html', context)