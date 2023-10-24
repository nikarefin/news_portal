from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
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


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'posts/subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
