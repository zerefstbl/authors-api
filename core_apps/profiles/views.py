from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.decorators import action

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
    serializers = {
        'default': ProfileSerializer,
        'update': UpdateProfileSerializer,
        'following': FollowingSerializer,
        'follow_unfollow': FollowingSerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializer_class)

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

        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        permission_classes=permission_classes,
        methods=['get', ],
        url_path='get-my-followers'
    )
    def get_my_followers(self, request, **kwargs):
        try:
            specific_user = self.queryset.get(user=request.user)
        except User.DoesNotExist:
            raise NotFound("Internal error ocurrered")

        userprofile_followers = specific_user.followed_by.all()

        serializer = self.get_serializer(userprofile_followers, many=True)

        formatted_response = {
            'status_code': status.HTTP_200_OK,
            'num_of_followers': len(serializer.data),
            'followers': serializer.data,
        }

        return Response(formatted_response, status=status.HTTP_200_OK)

    @action(
        detail=True,
        permission_classes=permission_classes,
        methods=['post', ],
        url_path='follow-and-unfollow',
    )
    def follow_and_unfollow(self, request, **kwargs):
        try:
            specific_user = self.queryset.get(user__username=self.kwargs.get('pk'))
        except User.DoesNotExist:
            raise NotFound('User with this name does not exist')

        current_user_profile = request.user.profile

        if specific_user.pkid == current_user_profile.pkid:
            raise CantFollowYourself

        if current_user_profile.check_following(specific_user):
            current_user_profile.unfollow(specific_user)

            formatted_response = {
                'status_code': status.HTTP_200_OK,
                'detail': f'Now you dont follow {specific_user.user.username}',
            }
            return Response(formatted_response, status=status.HTTP_200_OK)

        current_user_profile.follow(specific_user)

        formatted_response = {
            'status_code': status.HTTP_200_OK,
            'detail': f'You now follow {specific_user.user.username}',
        }

        return Response(formatted_response, status=status.HTTP_200_OK)
