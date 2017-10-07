import math
from unicodedata import decimal

from django.db import models

from booklist.models import Book

class Bind(models.Model):
    name = models.CharField(max_length=50)

    def get_bind_price(self, number_of_pages):
        range_for_pages = self.bindrange_set.filter(range_top__gte=number_of_pages).first()
        return range_for_pages.range_price if range_for_pages else 7


class BindRange(models.Model):
    bind = models.ForeignKey(Bind)
    range_top = models.PositiveIntegerField()
    range_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        ordering = ['range_top']

    def __str__(self):
        return str(self.range_top) + "-" + str(self.range_price)


class XeroPriceList(models.Model):
    name = models.CharField(max_length=50)

    def get_xero_per_page_price_range(self, number_of_pages):
        return self.xerorange_set.filter(range_top__gte=number_of_pages).first()


class XeroRange(models.Model):
    xero_price_list = models.ForeignKey(XeroPriceList)
    range_top = models.PositiveIntegerField()
    range_price_one_sided = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    range_price_two_sided = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        ordering = ['range_top']

    def __str__(self):
        return str(self.range_top) + "-" + str(self.range_price_one_sided) + "/" + str(self.range_price_two_sided)


class XeroList(models.Model):
    name = models.CharField(max_length=50, default="")
    xero_price_list = models.ForeignKey(XeroPriceList, default=None, null=True)

    def get_all_xero_pages(self):
        return sum([cost.number_of_pages for cost in self.get_all_xero_calcs()])

    def get_all_bind_cost(self):
        return sum([cost.bind_cost for cost in self.get_all_xero_calcs()])

    def get_all_cost_without_bind(self):
        return sum([cost.calc_xero_cost_without_bind() for cost in self.get_all_xero_calcs()])

    def get_all_cost_with_bind(self):
        return sum([cost.calc_xero_cost_with_bind() for cost in self.get_all_xero_calcs()])

    def get_all_quantity(self):
        return sum([cost.quantity for cost in self.get_all_xero_calcs()])

    def get_all_price_for_all_items(self):
        return sum([cost.price_for_all_items for cost in self.get_all_xero_calcs()])

    def add(self, xero_cost):
        xero_cost.xero_cost_list = self

    def get_all_xero_calcs(self):
        return [XeroCalc.get_xero_calc_by_id(id_["id"]) for id_ in self.xerocalc_set.values("id")]


class XeroCalc(models.Model):
    XERO_DEFAULT_COST_PER_PAGE_IN_GROSZ = 7
    XERO_COSTS = [6, 7, 8, 9, 10]
    BIND_COSTS = [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7]
    name = models.CharField(max_length=200, blank=True, null=True, default="")
    xero_cost_list = models.ForeignKey(XeroList, null=True)
    cost_per_page = models.DecimalField(max_digits=2, decimal_places=2, default=0)
    bind_cost = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    is_one_sided = models.BooleanField(default=True)
    is_two_sided = models.BooleanField(default=False)
    is_mix_with_two_sided_advantage = models.BooleanField(default=False)
    is_mix_with_one_sided_advantage = models.BooleanField(default=False)
    two_sided_pages_in_mix = models.PositiveIntegerField(default=0)
    one_sided_pages_in_mix = models.PositiveIntegerField(default=0)
    bind_ranges = models.ForeignKey(Bind, default=None)
    xero_cost_ranges = models.ForeignKey(XeroPriceList, default=None)
    cost_short_name = ''
    quantity = models.PositiveIntegerField(default=1)

    @property
    def price_for_all_items(self):
        return self.quantity * self.calc_xero_cost_with_bind()

    @property
    def all_pages(self):
        return self.number_of_pages * self.quantity

    @property
    def all_cards(self):
        return self.number_of_cards * self.quantity

    @property
    def number_of_pages(self):
        return 0

    @property
    def number_of_cards(self):
        return 0

    @property
    def is_mix(self):
        return self.is_mix_with_two_sided_advantage or self.is_mix_with_one_sided_advantage

    @property
    def cost_per_page_in_grosz(self):
        return int(self.cost_per_page * 100) if self.cost_per_page else self.XERO_DEFAULT_COST_PER_PAGE_IN_GROSZ

    @property
    def suggested_bind_cost(self):
        return self.bind_ranges.get_bind_price(self.number_of_cards if self.number_of_cards else 1)

    @property
    def suggested_xero_cost_per_page_in_grosz(self):
        return self.bind_ranges.get_bind_price(self.number_of_cards)

    @classmethod
    def get_xero_calc_by_id(cls, id_):
        calcs = cls.__subclasses__()
        return [calc.objects.get(xerocalc_ptr_id=id_) for calc in calcs
                if calc.objects.filter(xerocalc_ptr_id=id_).exists()][0] if XeroCalc.objects.filter(id=id_).exists() else None

    def calc_xero_cost_without_bind(self):
        return self.number_of_pages * self.cost_per_page

    def calc_xero_cost_with_bind(self):
        return self.calc_xero_cost_without_bind() + self.bind_cost



class XeroSimpleCalc(XeroCalc):

    number_of_cards_or_pages_from_form = models.PositiveIntegerField(default=0)

    is_cards_in_form = models.BooleanField(default=False)
    cost_short_name = 'simple'

    @property
    def number_of_pages_from_form(self):
        return self.number_of_cards_or_pages_from_form if not self.is_cards_in_form else 0

    @property
    def number_of_cards_from_form(self):
        return self.number_of_cards_or_pages_from_form if self.is_cards_in_form else 0

    @property
    def number_of_pages(self):
        if not self.is_cards_in_form:
            return self.number_of_pages_from_form
        base_pages = self.number_of_cards_from_form * (2 if self.is_two_sided or self.is_mix_with_two_sided_advantage else 1)
        additional_pages = 0 if not self.is_mix else (self.two_sided_pages_in_mix - self.one_sided_pages_in_mix)
        return base_pages + additional_pages

    @property
    def number_of_cards(self):
        if self.is_cards_in_form:
            return self.number_of_cards_from_form
        if self.is_one_sided:
            return self.number_of_pages_from_form
        if self.is_two_sided:
            return math.ceil(self.number_of_cards_or_pages_from_form/2)
        if self.is_mix_with_two_sided_advantage:
            return self.one_sided_pages_in_mix + (self.number_of_pages_from_form - self.one_sided_pages_in_mix)//2
        if self.is_mix_with_one_sided_advantage:
            return self.number_of_pages_from_form - self.two_sided_pages_in_mix

    @property
    def is_mix(self):
        return self.is_mix_with_two_sided_advantage or self.is_mix_with_one_sided_advantage


class XeroBookCalc(XeroCalc):
    book_pages_arabic = models.PositiveIntegerField(default=0)
    book_pages_roman = models.PositiveIntegerField(default=0)
    cost_short_name = 'book'
    is_two_to_one = models.BooleanField(default=True)

    @property
    def all_book_pages(self):
        return self.book_pages_arabic + self.book_pages_roman

    @property
    def number_of_pages(self):
        return int(math.ceil(self.all_book_pages/2)) if self.is_two_to_one else self.all_book_pages

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


class XeroByWeightCalc(XeroCalc):
    CARD_WEIGHT = 5
    BIND_COMBS_WEIGHTS = {8: 2, 10: 3, 12: 4, 14: 6, 16: 8, 19: 11, 22: 12, 25: 14, 28: 17, 32: 12, 38: 18, 45: 20, 51: 23}
    BIND_COMBS_RANGES = {6: range(1, 26), 8: range(26, 46), 10: range(46, 66), 12: range(66, 86), 14: range(86, 111),
                         16: range(111, 146), 19: range(146, 186), 22: range(186, 206), 25: range(206, 241),
                         28: range(241, 271), 32: range(271, 301), 38: range(301, 351), 45: range(351, 441),
                         51: range(441, 501)}
    BIND_FRONT_COVER_WEIGHTS = 13
    BIND_BACK_COVER_WEIGHTS = 15
    weight = models.PositiveIntegerField(default=0)
    is_bind = models.BooleanField(default=False)

    cost_short_name = 'weight'

    @property
    def bind_weight(self):
        return (self.BIND_BACK_COVER_WEIGHTS + self.BIND_FRONT_COVER_WEIGHTS + self.BIND_COMBS_WEIGHTS[self.calc_bind_size()]) \
            if self.is_bind else 0

    @property
    def number_of_cards(self):
        return self.cards_from_weight(self.weight - self.bind_weight)

    @property
    def number_of_pages(self):
        base_pages = self.number_of_cards * (2 if self.is_two_sided or self.is_mix_with_two_sided_advantage else 1)
        additional_pages = 0 if not self.is_mix else (self.two_sided_pages_in_mix - self.one_sided_pages_in_mix)
        return base_pages + additional_pages

    def calc_bind_size(self):
        default_size = 12
        weight_without_covers = self.weight - self.BIND_FRONT_COVER_WEIGHTS - self.BIND_BACK_COVER_WEIGHTS
        for size, comb_weight in self.BIND_COMBS_WEIGHTS.items():
            if self.cards_from_weight(weight_without_covers - comb_weight) in self.BIND_COMBS_RANGES[size]:
                return size
        return default_size

    @classmethod
    def cards_from_weight(cls, weight):
        return weight // cls.CARD_WEIGHT

