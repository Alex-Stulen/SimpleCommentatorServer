from django.contrib import admin

from . import models


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'reply_to', 'is_published')
    list_display_links = ('pk', 'username')
    search_fields = ('pk', 'username', 'email', 'text', 'file_path')
    readonly_fields = ('created_at', 'updated_at')
