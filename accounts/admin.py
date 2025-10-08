from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser 
from albums.models import Album, AlbumPhoto, AlbumEmail

class AlbumInline(admin.TabularInline):
    model = Album
    fields = ("title", "created_at")
    readonly_fields = ("created_at",)
    extra = 0
    show_change_link = True

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ("email", "first_name", "last_name", "user_type", "is_staff", "is_active")
    list_filter = ("user_type", "is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password", "first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "first_name", "last_name", "is_staff", "is_active", "groups", "user_permissions")}
        ),
    )

    inlines = [AlbumInline]


admin.site.register(CustomUser, CustomUserAdmin)