from django.db import models


class XeroCalc(models.Model):
    XERO_COSTS = [6, 7, 8, 9, 10]
    BIND_COSTS = [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6]
    number_of_pages = models.PositiveIntegerField(default=0)
    cost_per_page = models.DecimalField(max_digits=2, decimal_places=2)
    bind_cost = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        managed = False

    @property
    def cost_per_page_in_grosz(self):
        return int(self.cost_per_page * 100)

    def calc_xero_cost_without_bind(self):
        return self.number_of_pages * self.cost_per_page

    def calc_xero_cost_with_bind(self):
        return self.calc_xero_cost_without_bind() + self.bind_cost

