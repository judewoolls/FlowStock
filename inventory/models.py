from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    stock_code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Location(models.Model):
    LOCATION_TYPES = [
        ('CONSUMPTION', 'Consumption'),
        ('SHELF', 'Shelf'),
        ('QUARANTINE', 'Quarantine'),
        ('STOCKHOLD', 'Stockhold'),
        ('ACTIVE', 'Active'),
        ('DEFECTIVE', 'Defective')
    ]
    name = models.CharField(max_length=30)
    location_type = models.CharField(max_length=12, choices=LOCATION_TYPES)
    
    def __str__(self):
        return self.name

class Inventory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    
    class Meta:
        # This prevents duplicate rows for the same item in the same place
        constraints = [
            models.UniqueConstraint(fields=['item', 'location'], name='unique_item_at_location')
        ]

    def __str__(self):
        return f"{self.item.name} - {self.quantity} units @ {self.location.name}"
    
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('PUTAWAY', 'Putaway'), # Adding stock to inventory
        ('PICK', 'Pick'),         # Removing stock from inventory to fulfill an order
        ('ADJUST', 'Adjust'),    # Manual adjustment of stock levels (damage, loss, etc.)
        ('TRANSFER', 'Transfer'), # Moving stock between locations
        ('CONSUME', 'Consume') # Using stock for production or internal use
    ]
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(min_value=0)
    transaction_type = models.CharField(max_length=12, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    location_start = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='transaction_start', null=True, blank=True)
    location_end = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='transaction_end', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.transaction_type} - {self.item.stock_code} - {self.quantity} units from {self.location_start.name} to {self.location_end.name} on {self.timestamp}"