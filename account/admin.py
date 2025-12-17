# account/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Custom admin for your CustomUser model
class CustomUserAdmin(UserAdmin):
    # Fields and layout on the admin change form
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields displayed on the main list view
    list_display = ('email', 'first_name', 'last_name', 'is_staff')

    # Filters in the list view
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    # Searchable fields
    search_fields = ('email', 'first_name', 'last_name')

    # Default ordering
    ordering = ('email',)

# Register your CustomUser with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
