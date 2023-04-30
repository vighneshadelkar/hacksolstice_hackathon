from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(null=True, max_length = 255)
    email = models.EmailField()
    phone = models.IntegerField(null=True)
    last_logout = models.DateTimeField(blank=True, null=True)
    time_diff = models.IntegerField(blank=True, null=True)

    def _str_(self):
        return self.user.username
    
