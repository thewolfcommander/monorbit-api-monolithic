from django.contrib import admin

from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['mobile_number', 'email', 'full_name']
    list_filter = ['is_consumer', 'is_creator', 'is_working_profile', 'is_active', 'registered_on', 'updated_on', 'is_email_verified', 'is_mobile_verified', 'is_logged_in', 'last_logged_in_time', 'is_archived', 'is_agreed_to_terms', 'gender']
    search_fields = ['mobile_number', 'email', 'full_name']