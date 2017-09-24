import math
from django.db import models


class XeroCalc(models.Model):
    XERO_COSTS = [6, 7, 8, 9, 10]
    BIND_COSTS = [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6]
    name = models.CharField(max_length=200, blank=True, null=True, default="")

    cost_per_page = models.DecimalField(max_digits=2, decimal_places=2)
    bind_cost = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        managed = False

    @property
    def number_of_pages(self):
        return None

    @property
    def cost_per_page_in_grosz(self):
        return int(self.cost_per_page * 100)

    def calc_xero_cost_without_bind(self):
        return self.number_of_pages * self.cost_per_page

    def calc_xero_cost_with_bind(self):
        return self.calc_xero_cost_without_bind() + self.bind_cost


class XeroSimpleCalc(XeroCalc):
    number_of_pages_from_form = models.PositiveIntegerField(default=0)

    @property
    def number_of_pages(self):
        return self.number_of_pages_from_form


class XeroBookCalc(XeroCalc):
    book_pages_arabic = models.PositiveIntegerField(default=0)
    book_pages_roman = models.PositiveIntegerField(default=0)

    @property
    def all_book_pages(self):
        return self.book_pages_arabic + self.book_pages_roman

    @property
    def number_of_pages(self):
        return int(math.ceil(self.all_book_pages/2))




