from django.urls import path
from .views import ToggleLikeView, CommentListCreateView, CommentDeleteView

urlpatterns = [
    path('like/<int:pk>/', ToggleLikeView.as_view(), name='toggle_like'),
    path('comments/<int:pk>/', CommentListCreateView.as_view(), name='comments'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='delete_comment'),
]


