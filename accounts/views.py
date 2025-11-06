from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from albums import models
from albums.models import Album, AlbumEmail
from .forms import RegisterForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activează-ți contul MemoriX'

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = request.build_absolute_uri(reverse('activate', args=[uid, token]))

            html_message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })

            text_message = f"Salut {user.email},\nActivează-ți contul accesând acest link: {activation_link}"

            email = EmailMultiAlternatives(subject, text_message, settings.EMAIL_HOST_USER, [user.email])
            email.attach_alternative(html_message, "text/html")
            email.send()

            return render(request, 'accounts/activation_sent.html')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def activate_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'accounts/activation_success.html', {'user': user})
    else:
        return render(request, 'accounts/activation_invalid.html')

def profile_view(request):
    user = request.user

    try:
        user_email_obj = AlbumEmail.objects.get(email=user.email)
    except AlbumEmail.DoesNotExist:
        user_email_obj = None

    if user_email_obj:
        my_albums = Album.objects.filter(
            models.Q(user=user) | models.Q(emails=user_email_obj)
        ).distinct()
    else:
        my_albums = Album.objects.filter(user=user)

    context = {
        "my_albums": my_albums,
    }
    return render(request, "accounts/profile.html", context)

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if not email or not password:
            messages.error(request, "Completează email și parolă.")
            return render(request, "accounts/login.html", {"email": email})

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                if user.is_active:
                   login(request, user)
                   return redirect("profile")
            else:
                messages.warning(request, "Contul tău nu este activ. Verifică email-ul pentru activare.")
                return render(request, "accounts/login.html", {"email": email})
        else:
            messages.error(request, "Email sau parolă incorectă! Încearcă din nou.")
            return render(request, "accounts/login.html", {"email": email})

    return render(request, "accounts/login.html")
