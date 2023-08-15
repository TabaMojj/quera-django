from django.contrib import admin

from .models import BlockedIp, SecurityConfig, ViewDetail


# Register your models here.

@admin.register(BlockedIp)
class BlockedIpAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip', 'rps', 'view', 'ban_time', 'created_at')

    # Your code

    list_display_links = ('id', 'ip')


@admin.register(SecurityConfig)
class SecurityConfigAdmin(admin.ModelAdmin):
    # Your code
    pass


@admin.register(ViewDetail)
class ViewDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'path')

    search_fields = ('name', 'path')

    # Your code
