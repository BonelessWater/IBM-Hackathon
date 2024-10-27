# admin.py
from django.contrib import admin
from .models import User, InventoryItem

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'state')
    search_fields = ('username', 'email')
    list_filter = ('state',)

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
