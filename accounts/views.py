from .serializers import *
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from .models import *

from django.contrib.gis.geos import Point

# Create your views here.

class UserAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserRegistrationAPIView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': AuthToken.objects.create(user)[1]
        })


class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': AuthToken.objects.create(user)[1]
        })


class UserInfoAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserInfoSerializer

    def get_object(self):
        return UserInfo.objects.get(pk=self.request.user)

    def put(self, request, *args, **kwargs):
        user_info = self.get_object()

        serializer = self.get_serializer(user_info, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class UserContactAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserContactSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        id = request.data.pop('id', 0)
        try:
            instance = UserContacts.objects.get(pk=id)
        except UserContacts.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        id = request.data.pop('id', 0)
        try:
            instance = UserContacts.objects.get(pk=id)
        except UserContacts.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetailAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserDetailSerializer

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs['pk'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(user)

        return Response(serializer.data)



class UserSiteAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSiteSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        id = request.data.pop('id', 0)
        try:
            instance = UserSocialSites.objects.get(pk=id)
        except UserSocialSites.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        id = request.data.pop('id', 0)
        try:
            instance = UserSocialSites.objects.get(pk=id)
        except UserSocialSites.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)