from django.views.generic import ListView, DetailView
from .models import *


class PostList(ListView):
    model = Post
    template_name = 'news/post_list.html'
    context_object_name = 'post_list'
    ordering = '-date_joined'


class PostDetails(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'
