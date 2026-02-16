from django.urls import path
from .views import ToggleLikeView

urlpatterns = [
    path('like/<int:pk>/', ToggleLikeView.as_view(), name='toggle_like'),
]
