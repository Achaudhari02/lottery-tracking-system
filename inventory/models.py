from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Business (models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserProfile(models.Model):
    
    ROLES = {
        "WKR": "Worker",
        "OWNR": "Owner"
    }

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=4, choices=ROLES)
    stores = models.ManyToManyField(User)

class Store(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    store_code = models.CharField(max_length=100)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Game(models.Model):

    STATUSES = {
        "ACTIVE": "Active",
        "INACTIVE": "Inactive"
    }
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    game_number = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    ticket_price = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=8, choices=STATUSES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        constraints = [
            models.UniqueConstraint(fields=["business","game_number"])
        ]

class Pack(models.Model):
    
    STATUES = {
        "RS" : "Received",
        "AC" : "Active",
        "ST" : "Settled",
        "LS" : "Lost or Stolen"
    }

    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    barcode = models.CharField(max_length=100)
    starting_ticket = models.PositiveSmallIntegerField()
    ending_ticket = models.PositiveSmallIntegerField()
    last_ticket_sold= models.PositiveSmallIntegerField()
    status = models.CharField(max_length=2, choices=STATUES)
    current_location = models.CharField(max_length=100)
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL)
    received_at = models.DateTimeField() 
    activated_by = models.ForeignKey(User, on_delete=models.SET_NULL)
    activated_at = models.DateTimeField()
    settled_by = models.ForeignKey(User, on_delete=models.SET_NULL)
    settled_at = models.DateTimeField()
    lost_stolen_reason = models.CharField()
    lost_stolen_reported_by = models.ForeignKey(User, on_delete=models.SET_NULL)

class PackUpdate(models.Model):
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL)
    updated_at =models.DateTimeField(auto_now_add=True)
    previous_last_sold = models.PositiveSmallIntegerField()
    new_last_ticket = models.PositiveSmallIntegerField()
    

    




