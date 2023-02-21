from django.contrib import admin

from home.admin import BasketAdmin

from .models import EmailVerification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [BasketAdmin]


@admin.register(EmailVerification)
class EmailVerification(admin.ModelAdmin):
    list_display = ['user', 'code', 'created', 'expiration']
