from django.urls import path
from . import views

app_name = 'albums'

urlpatterns = [
    path('<uuid:share_token>/', views.album_view, name='album_view'),
]