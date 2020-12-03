from django.db import models
from django.contrib.gis.db import models as geo_models
from django.contrib.auth.models import User

# Create your models here.
class GiveAwayEvents(geo_models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    location = geo_models.PointField()
    headline = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    event_date_time = models.DateTimeField()
    event_posted = models.DateTimeField(auto_now_add=True)


def even_image_path(instance, filename):
    event_id = str(instance.event.id)

    return F"EventImages/{event_id}/{filename}"


class EventImages(models.Model):
    event = models.ForeignKey(GiveAwayEvents, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=even_image_path)


