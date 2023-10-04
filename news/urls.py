from django.urls import path
from news.views import *

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetails.as_view())
]
