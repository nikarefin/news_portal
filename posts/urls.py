from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path
from posts.views import *

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetails.as_view(), name='post_detail'),
    path('search', PostSearch.as_view(), name='post_search'),
    path('news/create', NewsAdd.as_view(), name='news_create'),
    path('news/<int:pk>/update', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete', NewsDelete.as_view(), name='news_delete'),
    path('article/create', ArticleAdd.as_view(), name='article_create'),
    path('article/<int:pk>/update', ArticleUpdate.as_view(), name='article_update'),
    path('article/<int:pk>/delete', ArticleDelete.as_view(), name='article_delete'),
]
