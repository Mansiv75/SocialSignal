from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Social_Media_Account(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    platform=models.CharField(max_length=100)
    access_token=models.CharField(max_length=255)
    refresh_token=models.CharField(max_length=255)
    expires_at=models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.platform}"
    
class SocialMediaStats(models.Model):
    account=models.ForeignKey(Social_Media_Account, on_delete=models.CASCADE)
    followers=models.IntegerField(null=True, blank=True)
    likes=models.IntegerField(null=True, blank=True)    
    last_update=models.DateTimeField(null=True, blank=True)