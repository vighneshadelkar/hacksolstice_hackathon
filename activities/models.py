from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
    
class Active(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active_time = models.IntegerField(default=0)
    date=models.DateField(default=timezone.now)