from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserProfileSerializer, FollowSerializer
from .models import User, Follow
from django.db.models import Q
from django.contrib.auth import get_user_model

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You are authenticated!"})

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class PublicProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

class FollowUserView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        following_user = serializer.validated_data['following']
        follower_user = self.request.user

        # Prevent self-follow
        if follower_user == following_user:
            raise serializers.ValidationError("You cannot follow yourself.")
        
        # Prevent duplicate follow
        if Follow.objects.filter(
            follower=follower_user,
            following=following_user
        ).exists():
            raise serializers.ValidationError("You already follow this user.")

        serializer.save(follower=follower_user)

User = get_user_model()

class UserSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.GET.get('q')

        if not query:
            return Response({"error": "Search query is required."}, status=400)

        users = User.objects.filter(
            Q(email__icontains=query) |
            Q(username__icontains=query)
        ).distinct()

        results = [
            {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "bio": user.bio
            }
            for user in users
        ]

        return Response(results)

class FollowersListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        followers = Follow.objects.filter(following_id=user_id)

        data = [
            {
                "id": follow.follower.id,
                "email": follow.follower.email,
                "username": follow.follower.username
            }
            for follow in followers
        ]

        return Response(data)


class FollowingListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        following = Follow.objects.filter(follower_id=user_id)

        data = [
            {
                "id": follow.following.id,
                "email": follow.following.email,
                "username": follow.following.username
            }
            for follow in following
        ]

        return Response(data)

