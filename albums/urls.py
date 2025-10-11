from django.urls import path
from . import views

app_name = 'albums'

urlpatterns = [
    path('view/<int:album_id>/', views.album_view, name='album_view'),
]
