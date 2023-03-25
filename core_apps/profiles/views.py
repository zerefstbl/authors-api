from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import CantFollowYourself, NotYourProfile
from .models import Profile
from .pagination import ProfilePagination
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import FollowingSerializer, ProfileSerializer, UpdateProfileSerializer

User = get_user_model()


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Profile.objects.select_related('user')
    renderer_classes = [ProfilesJSONRenderer, ]
    pagination_class = ProfilePagination

    def get_queryset(self):
        return Profile.objects.all()

    def get_object(self):
        try:
            username = self.kwargs.get('pk')
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('A profile with this username does not exist')

        return profile

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user != instance.user:
            print(instance.user.username)
            print(request.user)
            raise NotYourProfile

        serializer = UpdateProfileSerializer(instance=instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
