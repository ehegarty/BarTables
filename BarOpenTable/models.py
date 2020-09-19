from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Location(models.Model):
    name = models.CharField(unique=True, max_length=50)
    is_open = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Location, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Seat(models.Model):
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    capacity = models.IntegerField(default=2)
    is_free = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    number = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, to_field="id")
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT, to_field="id")
    time_in = models.TimeField(auto_now=False, auto_now_add=True)
    time_out = models.TimeField(auto_now=True, auto_now_add=False)
    date = models.DateField(auto_now=False, auto_now_add=True)
    u18 = models.BooleanField(default=False)
    person = models.IntegerField(default=0)

    def __str__(self):
        return self.first_name + " " + self.last_name + ", in: " + str(self.time_in) + ", out: " + str(self.time_out)
