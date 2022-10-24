from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uuid = models.IntegerField(null=False, default=1)
    Subject = models.CharField(max_length=200, null=True, blank=True)
    Location = models.CharField(max_length=200, null=True, blank=True)
    StartTime = models.DateTimeField(auto_now_add=False)
    EndTime = models.DateTimeField(auto_now_add=False)
