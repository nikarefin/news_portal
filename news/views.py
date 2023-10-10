from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .filters import PostFilter
from .forms import PostForm
from .models import *
from django.urls import reverse_lazy


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


class NewsCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post-create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NE'
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post-update.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'posts/post-delete.html'
    success_url = reverse_lazy('post_list')


class ArticleCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post-create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        return super().form_valid(form)


class ArticleUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post-update.html'


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'posts/post-delete.html'
    success_url = reverse_lazy('post_list')
