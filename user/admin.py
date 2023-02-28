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
        ('Permissions', {'fields': ('is_active','user_type', 'is_staff', 'groups')}),
        # ('Shoora Permissions', {'fields': ('roles',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'user_type', 'is_staff', 'organization'),
        }),
    )
    list_per_page = 20
    ordering = ('email',)
