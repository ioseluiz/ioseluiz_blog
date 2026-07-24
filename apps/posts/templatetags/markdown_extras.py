import markdown as md
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

_EXTENSIONS = [
    'fenced_code',
    'codehilite',
    'tables',
    'toc',
    'pymdownx.arithmatex',
]
_EXTENSION_CONFIGS = {
    'pymdownx.arithmatex': {'generic': True},
    'codehilite': {'guess_lang': False, 'use_pygments': True},
}


@register.filter(name='markdown')
def markdown_filter(value):
    rendered = md.markdown(
        value or '',
        extensions=_EXTENSIONS,
        extension_configs=_EXTENSION_CONFIGS,
    )
    return mark_safe(rendered)
