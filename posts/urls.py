from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path
from posts.views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(PostList.as_view()), name='post_list'),
    path('<int:pk>', cache_page(300)(PostDetails.as_view()), name='post_detail'),
    path('search', PostSearch.as_view(), name='post_search'),
    path('news/add', NewsAdd.as_view(), name='news_add'),
    path('news/<int:pk>/update', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete', NewsDelete.as_view(), name='news_delete'),
    path('article/add', ArticleAdd.as_view(), name='article_add'),
    path('article/<int:pk>/update', ArticleUpdate.as_view(), name='article_update'),
    path('article/<int:pk>/delete', ArticleDelete.as_view(), name='article_delete'),
]
