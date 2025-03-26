from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser


@admin.register(CustomUser)
class AdminCustomUser(UserAdmin):
    list_display = ['id',
                    'username',
                    'fio',
                    'phone',
                    'email',
                    'delete',
                    'is_active',
                    'is_staff']
    list_display_links = ['id', 'username']
    list_editable = ['is_active',
                     'is_staff']
    ordering = ['id', 'username']
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'middle_name', 'email', 'phone',)
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'delete', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined',)
        }),
    )