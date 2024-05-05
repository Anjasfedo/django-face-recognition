from django.db import models

from django.contrib.auth.models import User, Group
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length='50')
    profile_image = models.ImageField(
        default='default-avatar.png', upload_to='users/', null=True, blank=True)
    embedding = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.user.username
