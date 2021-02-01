from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Driver(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    vehicle = models.CharField(max_length=50)
    current_location = models.CharField(max_length=50)
    ride_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class DriveRequest(models.Model):
    customer_name = models.CharField(max_length=50)
    customer_phone = models.CharField(max_length=10)
    from_location = models.CharField(max_length=50)
    to_location = models.CharField(max_length=50)
    vehicle_preference = models.CharField(max_length=50)
    traveller_count = models.IntegerField()
    request_status= models.IntegerField(default=0)

    def __str__(self):
        return self.customer_name


class ConfirmedDrive(models.Model):
    driver_username = models.ForeignKey(Driver,on_delete=models.CASCADE)
    request_id = models.IntegerField()
    customer_name = models.CharField(max_length=50)
    customer_phone = models.CharField(max_length=10)
    from_location = models.CharField(max_length=50)
    to_location = models.CharField(max_length=50)
    one_time_password = models.IntegerField()

    def __str__(self):
        return self.customer_name
