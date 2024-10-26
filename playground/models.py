from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True, default='guest_user')
    password = models.CharField(max_length=128, default='')  # Store hashed passwords
    email = models.EmailField(unique=True, default='guest@example.com')
    address = models.CharField(max_length=255, default='N/A', blank=True, null=True)
    phone_number = models.CharField(max_length=15, default='000-000-0000', blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=150, default='N/A', blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, default='000-000-0000', blank=True, null=True)

    def __str__(self):
        return self.username
