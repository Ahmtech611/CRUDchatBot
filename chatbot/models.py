from django.db import models

class SystemUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=14, null=True, blank=True)
    city = models.CharField(max_length=80, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.email})"