from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from apps.posts.models import Post
from .forms import CommentForm


@login_required
@require_POST
def add_comment(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, published=True)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        messages.success(request, 'Tu comentario fue enviado y está pendiente de moderación.')
    return redirect('posts:detail', slug=post_slug)
