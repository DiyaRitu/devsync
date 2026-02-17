from django.urls import path
from .views import RegisterView, ProtectedView, ProfileView, PublicProfileView, FollowUserView, UserSearchView, FollowersListView, FollowingListView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/', PublicProfileView.as_view(), name='public_profile'),
    path('follow/', FollowUserView.as_view(), name='follow-user'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('users/<int:user_id>/followers/', FollowersListView.as_view()),
    path('users/<int:user_id>/following/', FollowingListView.as_view()),

]



