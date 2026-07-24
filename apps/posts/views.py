import os
import uuid

from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.storage import default_storage
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView

from .models import Post

ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB


@staff_member_required
@require_POST
def image_upload(request):
    file = request.FILES.get('image')
    if not file:
        return JsonResponse({'error': 'No se recibió ningún archivo.'}, status=400)
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        return JsonResponse({'error': 'Tipo de archivo no permitido. Usa JPG, PNG, GIF o WebP.'}, status=400)
    if file.size > MAX_IMAGE_SIZE:
        return JsonResponse({'error': 'La imagen no puede superar los 5 MB.'}, status=400)

    ext = os.path.splitext(file.name)[1].lower()
    filename = f'posts/content/{uuid.uuid4().hex}{ext}'
    saved_path = default_storage.save(filename, file)
    url = request.build_absolute_uri(default_storage.url(saved_path))
    return JsonResponse({'url': url})


class PostListView(ListView):
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        qs = Post.objects.filter(published=True)
        q = self.request.GET.get('q', '').strip()
        category = self.kwargs.get('category')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))
        if category:
            qs = qs.filter(category=category)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        ctx['current_category'] = self.kwargs.get('category', '')
        ctx['categories'] = Post.Category.choices
        return ctx


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(published=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comments'] = self.object.comments.filter(approved=True).order_by('created_at')
        return ctx
