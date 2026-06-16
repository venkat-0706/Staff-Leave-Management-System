from django.db import models
from django.contrib.auth.models import User 

class Profile(models.Model):
    ROLE_CHOICES = {
        ('admin','Admin'),
        ('staff','Staff'),
    }
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username 
    


