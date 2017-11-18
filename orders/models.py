from django.db import models

# Create your models here.


class Client(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    fb_profile = models.URLField()
    email = models.EmailField()


class Status(models.Model):
    name = models.CharField(max_length=200)

class Order(models.Model):

    client = models.ForeignKey(Client)
    status = models.ForeignKey(Status)
    