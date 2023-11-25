from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, unique=True)
    age = models.IntegerField(default=0, blank=True)
    sex = models.CharField(max_length=250, null=True, blank=True)
    blood_group = models.CharField(max_length=250, null=True, blank=True)
    fullname = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Reminder(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=True, blank=True)
    Days = models.CharField(max_length=250, null=True, blank=True) ## fri,thu,mon
    pillCount = models.IntegerField(default=0, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    time = models.CharField(max_length=250, null=True, blank=True)
    color_tag = models.CharField(max_length=250, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    
class Kyc(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    achievement = models.CharField(max_length=250, null=True, blank=True)
    location = models.CharField(max_length=250, null=True, blank=True)
    blood_group = models.CharField(max_length=250, null=True, blank=True)
    genotype = models.CharField(max_length=250, null=True, blank=True)
    medical_condition = models.CharField(max_length=250, null=True, blank=True)
    notification_type = models.CharField(max_length=250, null=True, blank=True)
    
    def __str__(self):
        return self.id
    
    
class Notification(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    title = models.TextField(blank=True,null=True)
    time = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=100,blank=True,null=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.profile.user.username} - {self.title}'
    
    
class Caregiver(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    fname = models.CharField(max_length=250, null=True, blank=True)
    lname = models.CharField(max_length=250, null=True, blank=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    
    def __str__(self):
        return self.id
    