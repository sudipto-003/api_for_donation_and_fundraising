from .models import *
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point


class EventSerializer(GeoFeatureModelSerializer):
    host = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = GiveAwayEvents
        geo_field = 'location'
        fields = ('id', 'host', 'location', 'headline', 'description', 'event_date_time')

    def create(self, validated_data):
        user = validated_data.pop('host')
        event = GiveAwayEvents.objects.create(host=user, **validated_data)

        return event

    def update(self, instance, validated_data):
        instance.location = validated_data.get('location', instance.location)
        instance.headline = validated_data.get('headline', instance.headline)
        instance.description = validated_data.get('description', instance.description)
        instance.event_date_time = validated_data.get('event_date_time', instance.event_date_time)
        instance.save()

        return instance


class FilteredEventSerializer(GeoFeatureModelSerializer):
    distance = serializers.SerializerMethodField()
    host = serializers.StringRelatedField()

    def get_distance(self, obj):
        return obj.distance.km

    class Meta:
        model = GiveAwayEvents
        geo_field = 'location'
        fields = ('headline', 'description', 'host', 'event_date_time', 'location', 'distance')