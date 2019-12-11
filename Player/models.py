from django.db import models


# Create your models here.
class User(models.Model):
    uname = models.CharField(max_length=100, blank=False, primary_key=True)
    fname = models.CharField(max_length=255, blank=False)
    lname = models.CharField(max_length=255, blank=False)
    phone = models.IntegerField()
    country = models.CharField(max_length=50, blank=False)
    address = models.TextField()
    city = models.CharField(max_length=50, blank=False)
    zip = models.IntegerField()
    bio = models.CharField(max_length=255, blank=False)
    email = models.CharField(max_length=100, blank=False)
    password = models.CharField(max_length=255, blank=False)


class Media(models.Model):
    uname = models.ForeignKey(User, on_delete=models.CASCADE, db_column='uname')
    f_name = models.CharField(max_length=255, blank=False)
    up_date = models.DateTimeField(blank=False)
    file = models.FileField(upload_to='%Y/%m/%d/', blank=False)


class Admin(models.Model):
    uname = models.CharField(max_length=100, blank=False, primary_key=True)
    password = models.CharField(max_length=255, blank=False)
    email = models.CharField(max_length=100, blank=False)
