from django.db import models
from django.contrib.auth.models import User 

class Leave(models.Model):
    STATUS_CHOICES = (
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected'),
    )
    DURATION_CHOICES = (
        ('full' , 'Full Day'),
        ('half' , 'Half Day')
    )
    HALF_DAY_CHOICES = (
        ('morning' , 'Morning'),
        ('afternoon' , 'Afternoon')
    )


    username = models.ForeignKey(User,on_delete = models.CASCADE)
    leave_type = models.CharField(max_length=100, default='Casual Leave')
    email = models.EmailField(blank=True, null=True)
    duration = models.CharField(max_length=20, choices = DURATION_CHOICES, default='full')
    half_day_session = models.CharField(max_length=20,choices=HALF_DAY_CHOICES, blank=True , null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.FloatField(default=0)
    reason = models.TextField()
    status = models.CharField(max_length=100, choices = STATUS_CHOICES , default = 'pending')


class LeaveBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_leave = models.FloatField(default=45)
    used_leave = models.FloatField(default=0)
    remaining_leave = models.FloatField(default=45)
    def save(self,*args,**kwargs):
        self.remaining_leave = (self.total_leave - self.used_leave)
        super().save(*args,**kwargs)
    

    def __str__(self):
        return self.username.username