from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import *

admin.site.register(Organization)

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("name","email","organization")
    exclude = ["user_permissions"]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'organization',)}),
        ('Django Permissions', {'fields': ('is_admin', 'is_active', 'is_staff', 'is_superuser')}),
        # ('Shoora Permissions', {'fields': ('roles',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'organization'),
        }),
    )
    list_per_page = 20
    ordering = ('email',)
