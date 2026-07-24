from django.urls import path
from .views import add_comment

app_name = 'comments'

urlpatterns = [
    path('post/<slug:post_slug>/comentar/', add_comment, name='add'),
]
