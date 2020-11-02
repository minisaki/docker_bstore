from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.BooleanField()
    birthday = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True, default='users/user_image.jpg')