from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .models import Donation, Project, WithdrawalRequest


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'owner',
                    'is_flexible', 'is_published',)
    search_fields = ('title', 'description',)
    list_filter = ('owner', 'is_flexible', 'is_published',)
    ordering = ('-created',)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'amount',
                    'created',)
    search_fields = ('user', 'created', 'project',)
    list_filter = ('user', 'project',)
    ordering = ('-created',)


@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'paid', 'created',)
    search_fields = ('user', 'project',)
    list_filter = ('paid', 'user',)
    ordering = ('-created',)
