"""Users admin."""
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import AppUser


class MyUserAdmin(UserAdmin):
    """
    Admin back end class.

    This is for handling Django admin create user.
    """

    model = AppUser

    list_display = ['email', 'person_type', 'company_id', 'site', 'is_active']

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    fieldsets = (
        (_('Personal info'), {'fields': ('email', 'password', 'site',
                                         'primary',
                              'person_type', 'email_verified', 'company_id')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
                            'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',
                                'password_changed')}),
        (_('Groups'), {'fields': ('groups',)}),
    )

    add_fieldsets = (
        (_('Create Account'), {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'site',
                       'email_verified', 'person_type', 'company_id')}
         ),
    )


admin.site.register(AppUser, MyUserAdmin)


def admin_login(request, extra_context=None):
    """Redirect to default login view which enforces auth policy."""
    next_page = request.get_full_path()
    next_url = next_page.split('=')[1] if '=' in next_page else next_page
    q = REDIRECT_FIELD_NAME + '=' + next_url
    return HttpResponseRedirect(reverse('login') + '?' + q)


admin.site.login = admin_login


def admin_logout(request, extra_context=None):
    """Redirect to default login page and not /admin area."""
    return HttpResponseRedirect(reverse('login'))


admin.site.logout = admin_logout
