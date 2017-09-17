from django.db import models


class XeroCalc(models.Model):
    number_of_pages = models.PositiveIntegerField(default=0)
    cost_per_page = models.DecimalField(max_digits=2, decimal_places=2)
    bind_cost = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        managed = False

    def calc_xero_cost_without_bind(self):
        return self.number_of_pages * self.cost_per_page

    def calc_xero_cost_with_bind(self):
        return self.calc_xero_cost_without_bind() + self.bind_cost

