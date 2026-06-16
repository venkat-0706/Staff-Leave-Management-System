from django.db import models
from django.contrib.auth.models import User 

class Leave(models.Model):
    STATUS_CHOICES = (
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected'),
    )

    username = models.ForeignKey(User,on_delete = models.CASCADE)
    leave_type = models.CharField(max_length=100, default='Casual Leave')
    email = models.EmailField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=100, choices = STATUS_CHOICES , default = 'pending')

    def __str__(self):
        return self.username.username