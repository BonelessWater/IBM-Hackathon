from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    STATE_CHOICES = [
        ('neither', 'Neither'),
        ('helper', 'Helper'),
        ('help', 'Need Help'),
    ]

    address = models.CharField(max_length=255, default='N/A', blank=True, null=True)
    phone_number = models.CharField(max_length=15, default='000-000-0000', blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=150, default='N/A', blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, default='000-000-0000', blank=True, null=True)
    state = models.CharField(max_length=15, choices=STATE_CHOICES, default='neither')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True
    )

    def __str__(self):
        return self.username

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (x{self.quantity})"
