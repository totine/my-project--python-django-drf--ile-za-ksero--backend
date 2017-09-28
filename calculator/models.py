import math
from django.db import models

from booklist.models import Book

class Bind(models.Model):
    name = models.CharField(max_length=50)

    def get_bind_price(self, number_of_pages):
        range_for_pages = self.bindrange_set.filter(range_top__gte=number_of_pages).first()
        return range_for_pages.range_price


class BindRange(models.Model):
    bind = models.ForeignKey(Bind)
    range_top = models.PositiveIntegerField()
    range_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        ordering = ['range_top']

class XeroList(models.Model):

    def get_all_xero_pages(self):
        return sum([cost.number_of_pages for cost in self.get_all_xero_calcs()])

    def get_all_bind_cost(self):
        return sum([cost.bind_cost for cost in self.get_all_xero_calcs()])

    def get_all_cost_without_bind(self):
        return sum([cost.calc_xero_cost_without_bind for cost in self.get_all_xero_calcs()])

    def get_all_cost_with_bind(self):
        return sum([cost.calc_xero_cost_with_bind for cost in self.get_all_xero_calcs()])

    def add(self, xero_cost):
        xero_cost.xero_cost_list = self

    def get_all_xero_calcs(self):
        return [XeroCalc.get_xero_calc_by_id(id_["id"]) for id_ in self.xerocalc_set.values("id")]


class XeroCalc(models.Model):

    XERO_COSTS = [6, 7, 8, 9, 10]
    BIND_COSTS = [0, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6]
    name = models.CharField(max_length=200, blank=True, null=True, default="")
    xero_cost_list = models.ForeignKey(XeroList, null=True)
    cost_per_page = models.DecimalField(max_digits=2, decimal_places=2, default=0)
    bind_cost = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    is_one_sided = models.BooleanField(default=False)
    is_two_sided = models.BooleanField(default=False)
    bind_ranges = models.ForeignKey(Bind, default=None)

    @property
    def number_of_pages(self):
        return 0

    @property
    def number_of_cards(self):
        return 0

    @property
    def cost_per_page_in_grosz(self):
        return int(self.cost_per_page * 100) if self.cost_per_page else 0

    @property
    def suggested_bind_cost(self):
        return self.bind_ranges.get_bind_price(self.number_of_cards)

    @classmethod
    def get_xero_calc_by_id(cls, id_):
        calcs = cls.__subclasses__()
        return [calc.objects.get(xerocalc_ptr_id=id_) for calc in calcs
                if calc.objects.filter(xerocalc_ptr_id=id_).exists()][0]

    def calc_xero_cost_without_bind(self):
        return self.number_of_pages * self.cost_per_page

    def calc_xero_cost_with_bind(self):
        return self.calc_xero_cost_without_bind() + self.bind_cost


class XeroSimpleCalc(XeroCalc):

    number_of_cards_from_form = models.PositiveIntegerField(default=0)
    is_mix_with_two_sided_advantage = models.BooleanField(default=False)
    is_mix_with_one_sided_advantage = models.BooleanField(default=False)
    two_sided_pages_in_mix = models.PositiveIntegerField(default=0)
    one_sided_pages_in_mix = models.PositiveIntegerField(default=0)

    @property
    def number_of_pages(self):
        base_pages = self.number_of_cards_from_form * (2 if self.is_two_sided or self.is_mix_with_two_sided_advantage else 1)
        additional_pages = 0 if not self.is_mix else (self.two_sided_pages_in_mix - self.one_sided_pages_in_mix)
        return base_pages - additional_pages

    @property
    def number_of_cards(self):
        return self.number_of_cards_from_form

    @property
    def is_mix(self):
        return self.is_mix_with_two_sided_advantage or self.is_mix_with_one_sided_advantage


class XeroBookCalc(XeroCalc):
    book_pages_arabic = models.PositiveIntegerField(default=0)
    book_pages_roman = models.PositiveIntegerField(default=0)

    @property
    def all_book_pages(self):
        return self.book_pages_arabic + self.book_pages_roman

    @property
    def number_of_pages(self):
        return int(math.ceil(self.all_book_pages/2))

    @property
    def number_of_cards(self):
        return self.number_of_pages if self.is_one_sided else int(math.ceil(self.number_of_pages/2))


class XeroBaseBookCalc(XeroCalc):

    book = models.ForeignKey(Book, default=None)
    xero_pages_real = models.IntegerField(default=0)

    @property
    def book_pages_arabic(self):
        return self.book.number_of_pages.arabic

    @property
    def book_pages_roman(self):
        return self.book.number_of_pages.roman

    @property
    def number_of_cards_real(self):
        return int(math.ceil(self.xero_pages_real/2))

