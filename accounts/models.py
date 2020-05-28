from django.db import models
from django.contrib.gis.db import models as geo_models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.
def user_image_path(instance, filename):
    user_name = instance.user.username

    return F"UserImages/{user_name}/{filename}"

class UserInfo(geo_models.Model):
    user = geo_models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='user_info')
    location = geo_models.PointField(null=True, blank=True)
    image = geo_models.ImageField(upload_to=user_image_path, null=True, blank=True)


def auto_create_userinfo(sender, **kwargs):
    user = kwargs['instance']

    if kwargs['created']:
        userinfo = UserInfo(user=user)
        userinfo.save()

post_save.connect(auto_create_userinfo, sender=User)


class UserContacts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_contacts')
    number = models.CharField(max_length=15, unique=True)


class UserSocialSites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sites')
    address = models.URLField(unique=True)