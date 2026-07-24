from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ('author', 'post', 'approved', 'created_at')
    list_filter   = ('approved',)
    search_fields = ('author__username', 'post__title', 'content')
    list_editable = ('approved',)
    readonly_fields = ('created_at',)
    actions = ['approve_comments', 'reject_comments']

    @admin.action(description='Aprobar comentarios seleccionados')
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

    @admin.action(description='Rechazar comentarios seleccionados')
    def reject_comments(self, request, queryset):
        queryset.update(approved=False)
