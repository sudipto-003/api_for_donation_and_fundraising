from .serializers import *
from .models import *
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

class EventAPIView(generics.GenericAPIView):
    permissions = (permissions.IsAuthenticated, )
    serializer_class = EventSerializer

    def post(self, request, *args, **kwargs):
        request.data['host'] = request.user.id
        coordinates = request.data.pop('location')
        longitude, latitute = coordinates
        point = Point(float(longitude), float(latitute))
        request.data['location'] = point
        instance = self.get_serializer(data=request.data)
        instance.is_valid(raise_exception=True)
        instance.save()
        
        return Response(instance.data)


class EventDetailAPIView(generics.GenericAPIView):
    permissions = (permissions.IsAuthenticated, )
    serializer_class = EventSerializer

    def put(self, request, *args, **kwargs):
        try:
            event = GiveAwayEvents.objects.get(id=kwargs['pk'])
            coordinates = request.data.get('location', None)
            if coordinates is not None:
                longitude, latitute = coordinates
                point = Point(float(longitude), float(latitute))
                request.data['location'] = point
            serializer = self.get_serializer(event, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)
        
        except GiveAwayEvents.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    
    def delete(self, request, *args, **kwargs):
        try:
            event = GiveAwayEvents.objects.get(id=kwargs['pk'])
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except GiveAwayEvents.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



class NearEventsAPIView(generics.GenericAPIView):
    permissions = (permissions.IsAuthenticated, )
    serializer_class = FilteredEventSerializer

    def get(self, request, *args, **kwargs):
        user_location = request.user.user_info.location
        circle_radius = request.query_params.get('radius', 10)
        near_events = GiveAwayEvents.objects.filter(location__distance_lte=(
            user_location, D(km=circle_radius))).annotate(distance=Distance(
                'location', user_location
            ))
        serializer = self.get_serializer(near_events, many=True)

        return Response(serializer.data)
