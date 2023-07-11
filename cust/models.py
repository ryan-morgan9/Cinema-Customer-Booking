from django.db import models
from django.contrib.auth.models import User
    
class PaymentDetails(models.Model):
    cardholderName = models.CharField(max_length=100)
    cardNumber = models.IntegerField()
    expiryDate = models.CharField(max_length=5)
    cardType = models.CharField(max_length=6)

class Screen(models.Model):
    capacity = models.IntegerField()

class Showings(models.Model):
    showingDate = models.DateField()
    showingTime = models.TimeField(default='12:00:00')
    filmTitle = models.CharField(max_length=100)
    ageRating = models.IntegerField()
    filmDuration = models.FloatField()
    trailerDescription = models.CharField(max_length=400)
    ticketsSold = models.IntegerField()
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    sociallyDistanced = models.BooleanField(default=False)

class Booking(models.Model):
    showingRef = models.ForeignKey(Showings, on_delete=models.CASCADE)
    ticketQuantity = models.IntegerField()
    totalCost = models.FloatField()
    paymentRef = models.ForeignKey(PaymentDetails, on_delete=models.CASCADE)

