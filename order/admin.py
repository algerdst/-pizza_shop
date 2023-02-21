from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'initiator', 'first_name', 'number', 'address', 'created', 'content']
