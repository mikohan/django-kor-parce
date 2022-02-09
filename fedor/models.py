from django.db import models

# Create your models here.


class Fedor(models.Model):

    productUrl = models.CharField(max_length=500, primary_key=True)
    title = models.CharField(max_length=255)
    imgUrl = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField()
    price = models.FloatField()
    brand = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title
