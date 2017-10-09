from django.db import models


class Customer:
    pass

class Order:
    customer = models.OneToOneField(Customer)
