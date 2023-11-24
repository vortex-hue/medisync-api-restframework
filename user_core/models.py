from django.db import models
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
    

    