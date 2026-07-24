from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display    = ('title', 'category', 'author', 'published', 'created_at')
    list_filter     = ('category', 'published')
    search_fields   = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable   = ('published',)
    readonly_fields = ('created_at', 'updated_at')

    class Media:
        css = {
            'all': [
                'https://cdn.jsdelivr.net/npm/easymde/dist/easymde.min.css',
                'admin/css/easymde_dark.css',
            ]
        }
        js = [
            'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js',
            'https://cdn.jsdelivr.net/npm/easymde/dist/easymde.min.js',
            'admin/js/easymde_init.js',
        ]
