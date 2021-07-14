from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import TextField


User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)