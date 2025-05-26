from django.contrib.auth.models import User
from django.db import models

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)
    location = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    guest_capacity = models.IntegerField(default=1)
    image = models.ImageField(upload_to='listing_images/', blank=True, null=True)


    def __str__(self):
        return self.title

from django.contrib.auth.models import User

class Booking(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.listing.title} ({self.check_in} to {self.check_out})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    id_or_passport_number = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username
