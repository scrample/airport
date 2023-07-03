from django.db import models
from django.urls import reverse
from django.db.models.base import Model
from django.db.models.deletion import PROTECT
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Airport(models.Model):
    PORT_CHOICES = (
        ('Far away airport','Far away airport'),
        ('Close airport','Close airport'),
        ('Strange airport','Strange airport'),
        ('World Pain airport','World Pain airport'),
        ('Miami airport','Miami airport'),
        ('Moscow airport','Moscow airport')
    )
    airportname = models.CharField(max_length=50, choices=PORT_CHOICES)

    def __str__(self):
        return self.airportname


class FlightRace(models.Model):
    RaceNumber = models.CharField(max_length=30)
    FROM_CHOICES = (
        ('This airport','This airport'),
    )
    From = models.CharField(max_length=50, choices=FROM_CHOICES)
    To = models.ForeignKey(Airport, on_delete=models.CASCADE)
    Price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.RaceNumber


class Company(models.Model):
    COMPANY_CHOICES = (
        ('11 SEPTEMBER COMPANY','11 SEPTEMBER COMPANY'),
        ('ALIBABA Inc','ALIBABA Inc'),
        ('AIR BOMB Corp.','AIR BOMB Corp.'),
        ('We will die Inc','We will die Inc')
    )
    companyname = models.CharField(max_length=50, choices=COMPANY_CHOICES)

    def __str__(self):
        return self.companyname


class AirPlane(models.Model):
    planenumber = models.CharField(max_length=30)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    def __str__(self):
        return self.planenumber


class Flight(models.Model):
    Race = models.ForeignKey(FlightRace, on_delete=models.CASCADE)
    startTime = models.DateTimeField(null=False)
    plane = models.ForeignKey(AirPlane, on_delete=models.CASCADE)

    def get_From(self):
        return self.Race.From

    def get_To(self):
        return self.Race.To

    def get_Date(self):
        return self.startTime.date()

    def get_Time(self):
        return self.startTime.time()

    def get_Price(self):
        return self.Race.Price
        
    def get_Name(self):
        return self.Race.RaceNumber
    
    def __str__(self):
        return self.Race.RaceNumber
    

class Ticket(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    SEAT_CHOICES = (
        ('1A','1A'), ('2A','2A'),
        ('1B','1B'), ('2B','2B'),
        ('1C','1C'), ('2C','2C'),
        ('1D','1D'), ('2D','2D'),
        ('1E','1E'), ('2E','2E'),
    )
    seat = models.CharField(max_length=50, choices=SEAT_CHOICES)
    available = models.BooleanField(default=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    