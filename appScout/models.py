from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission,User

# Create your models here.


class Conto(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cash=models.FloatField(default=0.0)
    carta=models.FloatField(default=0.0)
    conto = models.FloatField(default=0.0)

class Spesa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data=models.DateField(null=False)
    quanto=models.FloatField(null=False)
    dove=models.TextField(null=False)
    note=models.TextField()
    cosa=models.TextField(null=False)
    cartacash=models.BooleanField(null=False)

    def __str__(self):
        return f"{self.cosa} - {self.quanto} - {self.data}"


class Persona(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data=models.DateField(null=False)
    cognome=models.TextField(null=False)
    sex=models.BooleanField(null=False)
    note=models.TextField()
    nome=models.TextField(null=False)
