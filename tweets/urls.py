from django.urls import path
from .views import *

app_name="tweets"
urlpatterns = [
    path('', tweet_list_view),
    path('action/', tweet_action_view),
    path('create/', tweet_create_view),
    path('<int:id>/', tweet_detail_view),
    path('<int:id>/delete/', tweet_delete_view),
    path('<int:pk>/update/', TweetUpdateView.as_view()),
]
