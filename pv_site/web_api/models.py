from django.db import models


# Create your models here.
class Yield(models.Model):
    plz = models.CharField(max_length=5)
    pv_yield = models.FloatField()
