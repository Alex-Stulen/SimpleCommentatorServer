from django.urls import path

from . import views

urlpatterns = [
    path('comments/', views.CommentsAPIView.as_view()),
    path('comments/<int:comment_id>/', views.CommentAPIView.as_view()),
    path('comments/<int:comment_id>/replies/', views.CommentRepliesAPIView.as_view()),
]
