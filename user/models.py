from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        ADMIN = "admin", "Admin"
        CUSTOMER = "customer", "Customer"

    role = models.CharField(max_length=32, choices=RoleChoices.choices, default=RoleChoices.CUSTOMER)

    def __str__(self):
        return self.username