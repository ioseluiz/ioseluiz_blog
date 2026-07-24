from django.contrib import admin
from django.utils.html import format_html
from .models import Animation, Post


@admin.register(Animation)
class AnimationAdmin(admin.ModelAdmin):
    list_display    = ('title', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'embed_code')
    fields          = ('title', 'slug', 'html_file', 'created_at', 'embed_code')

    def embed_code(self, obj):
        if not obj.html_file:
            return '— Guarda primero para ver el código.'
        url = obj.html_file.url
        iframe = f'<iframe src="{url}" width="700" height="500" frameborder="0" allowfullscreen></iframe>'
        return format_html(
            '<textarea onclick="this.select()" style="width:100%;height:72px;'
            'font-family:monospace;font-size:0.82rem;padding:8px;'
            'background:#1e1e2e;color:#cdd6f4;border:1px solid #45475a;'
            'border-radius:4px;resize:vertical">{}</textarea>',
            iframe,
        )
    embed_code.short_description = 'Código iframe (clic para seleccionar → Ctrl+C)'


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
