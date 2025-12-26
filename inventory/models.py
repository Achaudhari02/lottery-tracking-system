from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.

class Business (models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User,on_delete=models.PROTECT, related_name="owned_businesses")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Name: {self.name} Owner: {self.owner}"

class Store(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="stores")
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    store_code = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Name: {self.name} business: {self.business.name}'

class UserProfile(models.Model):
    
    ROLES = {
        "WKR": "Worker",
        "OWNR": "Owner"
    }

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=4, choices=ROLES)
    stores = models.ManyToManyField(Store, related_name="assigned_stores", blank=True)

    def __str__(self):
        store_names = ",".join(self.stores.values_list("name",flat=True))
        return f"Role: {self.role} Store(s): {store_names}"


class Game(models.Model):

    STATUSES = {
        "ACTIVE": "Active",
        "ENDED": "ENDED"
    }
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="games")
    game_number = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=8, choices=STATUSES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tickets_per_pack = models.PositiveSmallIntegerField()

    class Meta:

        constraints = [
            models.UniqueConstraint(fields=["business","game_number"], name="unique_game_per_business")
        ]
    def __str__(self):
        return f"Name: {self.name} Price: {self.ticket_price} Status: {self.status}"

class Pack(models.Model):
    
    STATUSES = {
        "RS" : "Received",
        "AC" : "Active",
        "ST" : "Settled",
        "LS" : "Lost or Stolen"
    }

    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name="packs")
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name="packs")
    # pack barcode xxxx-xxxxxxx-xxx game-pack-ticket
    barcode = models.CharField(max_length=100, unique=True, validators= [
        RegexValidator(
            regex=r'^\d{4}-\d{7}-\d{3}$',
            message="Please enter a valid barcode. Barcode must be in the following format (Digits only): xxxx-xxxxxxx-xxx",
            code="invalid_barcode"
        )
    ],
    )
    # pack number extracted from the barcode
    pack_number = models.PositiveIntegerField()
    # the starting ticket number typically 000
    starting_ticket = models.PositiveSmallIntegerField()
    # the number of the last ticket in the pack
    ending_ticket = models.PositiveSmallIntegerField()
    # the current ticket the pack in on 
    current_ticket= models.PositiveSmallIntegerField(null=True, blank=True)
    # previous ticket number at shift close
    previous_ticket = models.PositiveSmallIntegerField(null=True,blank=True)
    status = models.CharField(max_length=2, choices=STATUSES)
    # physical box number that the pack is located in
    current_location = models.PositiveSmallIntegerField(max_length=100,blank=True,null=True)
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name="received_packs",null=True)
    received_at = models.DateTimeField(auto_now_add=True) 
    activated_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name="activated_packs",null=True,blank=True)
    activated_at = models.DateTimeField(null=True,blank=True)
    settled_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name="settled_packs",null=True,blank=True)
    settled_at = models.DateTimeField(null=True,blank=True)
    lost_stolen_reason = models.CharField(max_length=500, blank=True)
    lost_stolen_reported_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name="lost_packs",null=True,blank=True)
    lost_stolen_reported_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"Store: {self.store.name} Game: {self.game.name}"
    

    @property
    def total_tickets_sold(self):
        if self.current_ticket == None: 
            return 0
        return self.current_ticket
    
    @property
    def tickets_remaining(self):
        if self.current_ticket == None: 
            return self.ending_ticket + 1
        return (self.ending_ticket - self.current_ticket) + 1
    
    @property
    def percent_complete(self):
        if self.current_ticket == None or self.current_ticket == 0: 
            return 0.00
        percentage = ((self.current_ticket) / (self.ending_ticket + 1)) * 100
        return percentage

class PackUpdate(models.Model):
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE, related_name="updates")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="pack_updates_created", null=True)
    updated_at =models.DateTimeField(auto_now_add=True)
    previous_last_sold = models.PositiveSmallIntegerField(null=True,blank=True)
    new_last_ticket = models.PositiveSmallIntegerField()
    tickets_sold_this_update = models.PositiveSmallIntegerField()
    #do not need the notes field 

    class Meta: 
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Updated by: {self.updated_by.username}"
    

    




