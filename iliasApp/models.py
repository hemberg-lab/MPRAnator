from django.db import models

# Create your models here.

class SampleCounting(models.Model):
    num = models.IntegerField(default=0)
