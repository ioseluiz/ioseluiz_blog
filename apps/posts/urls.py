from django.urls import path
from .views import PostListView, PostDetailView, image_upload

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('categoria/<str:category>/', PostListView.as_view(), name='by_category'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='detail'),
    path('upload-imagen/', image_upload, name='image_upload'),
]
