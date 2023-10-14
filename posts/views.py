from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .filters import PostFilter
from .forms import PostForm
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostList(ListView):
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'
    ordering = '-date_joined'
    paginate_by = 10


class PostDetails(DetailView):
    model = Post
    template_name = 'posts/post.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    template_name = 'posts/search.html'
    context_object_name = 'posts'
    ordering = '-date_joined'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsAdd(CreateView, PermissionRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = 'posts/post-add.html'
    permission_required = ('posts.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NE'
        return super().form_valid(form)


class NewsUpdate(UpdateView, PermissionRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = 'posts/post-update.html'
    permission_required = ('posts.update_post',)


class NewsDelete(DeleteView, PermissionRequiredMixin):
    model = Post
    template_name = 'posts/post-delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('posts.delete_post',)


class ArticleAdd(CreateView, PermissionRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = 'posts/post-add.html'
    permission_required = ('posts.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        return super().form_valid(form)


class ArticleUpdate(UpdateView, PermissionRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = 'posts/post-update.html'
    permission_required = ('posts.update_post',)


class ArticleDelete(DeleteView, PermissionRequiredMixin):
    model = Post
    template_name = 'posts/post-delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('posts.delete_post',)
