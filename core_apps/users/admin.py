from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import UserChangeFormm, UserCreationForm
from .models import User

class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    add_form = UserCreationForm
    form = UserChangeFormm
    model = User
    list_display = [
        'pkid',
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
    ]
    list_display_links = [
        'id',
        'email',
    ]
    list_filter = [
        'email',
        'username',
        'first_name',
        'last_name',
        'is_staff',
    ]
    fieldsets = (
        (
            _('Login Credentials'),
            {
                'fields': (
                    'email',
                    'password',
                    
                )
            },
        ),
        (
            _('Personal Informationm'),
            {
                'fields': (
                    'username',
                    'first_name',
                    'last_name',
                )
            },
        ),
        (
            _('Permissions and Groups'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            },
        ),
        (
            _('Important Dates'),
            {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            },
        ),
    )