from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Animation(models.Model):
    title      = models.CharField(max_length=200, verbose_name='Título')
    slug       = models.SlugField(max_length=220, unique=True, blank=True)
    html_file  = models.FileField(upload_to='animations/', verbose_name='Archivo HTML')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Animación'
        verbose_name_plural = 'Animaciones'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Post(models.Model):
    class Category(models.TextChoices):
        SOFTWARE   = 'software',   'Desarrollo de Software'
        STRUCTURAL = 'structural', 'Ingeniería Estructural'

    title       = models.CharField(max_length=200, verbose_name='Título')
    slug        = models.SlugField(max_length=220, unique=True, blank=True)
    content     = models.TextField(verbose_name='Contenido (Markdown)')
    category    = models.CharField(
        max_length=20,
        choices=Category.choices,
        verbose_name='Categoría',
    )
    author      = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Autor',
    )
    cover_image = models.ImageField(
        upload_to='posts/covers/',
        blank=True,
        null=True,
        verbose_name='Imagen de portada',
    )
    published   = models.BooleanField(default=False, verbose_name='Publicado')
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated_at  = models.DateTimeField(auto_now=True, verbose_name='Actualizado')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
