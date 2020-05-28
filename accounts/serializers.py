from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )

        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)

        if user:
            return user

        return serializers.ValidationError("Incorrect Credentials")


class UserInfoSerializer(GeoFeatureModelSerializer):
    #user = UserSerializer()

    class Meta:
        model = UserInfo
        geo_field = 'location'
        id_field = False
        fields = ('location', 'image')

    def to_internal_value(self, data):
        longitude = data.get('longitude')
        latitude = data.get('latitude')
        image = data.get('image')

        final_data = {}

        if longitude is not None and latitude is not None:
            final_data['location'] = Point(float(longitude), float(latitude))
        if image:
            final_data['image'] = image
        
        return final_data

    def update(self, instance, validated_data):
        instance.location = validated_data.get('location', instance.location)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        return instance


class UserContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserContacts
        fields = ('id', 'number', )


class UserSiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSocialSites
        fields = ('id', 'address', )


class UserDetailSerializer(serializers.ModelSerializer):
    user_info = UserInfoSerializer()
    user_contacts = UserContactSerializer(many=True)
    user_sites = UserSiteSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'user_info', 'user_contacts', 'user_sites')