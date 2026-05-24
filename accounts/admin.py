from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display  = ['username', 'email', 'role', 'is_staff']
    list_filter   = ['role', 'is_staff']
    search_fields = ['username', 'email']
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Profile', {'fields': ('role', 'profile_pic')}),
    )