# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Tenant(models.Model):
    tenant_id = models.CharField(max_length=100, unique=True)
    domain = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.tenant_id

class Organization(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

class Department(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

class Customer(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
