# users/admin.py

from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'state']
    search_fields = ['user__username', 'phone', 'city', 'state']