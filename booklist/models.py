from django.db import models
from django.db.models.signals import post_save
import math
from decimal import Decimal


class Person(models.Model):
    firstname = models.CharField(max_length=50)
    secondname = models.CharField(max_length=50, default="", blank=True)
    surname = models.CharField(max_length=50)

    def __str__(self):
        return " ".join([self.firstname, self.secondname, self.surname])

    def getFullName(self):
        return " ".join([self.firstname, self.secondname, self.surname])


class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    full_name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=30, default=None, null=True)
    city = models.ForeignKey(City)

    def __str__(self):
        return self.full_name


class Edition(models.Model):
    number = models.PositiveIntegerField(default=1)
    year = models.PositiveIntegerField()
    comment = models.CharField(max_length=50, default="", blank=True)

    def __str__(self):
        return str(self.number) + ". " + str(self.year)


class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ForeignEdition(models.Model):
    language = models.ForeignKey(Language, default=None)
    number = models.PositiveIntegerField(default=1)
    year = models.PositiveIntegerField()
    publisher = models.ForeignKey(Publisher)
    translator = models.ManyToManyField(Person)


class BookSeries(models.Model):
    name = models.CharField(max_length=100)
    publisher = models.ForeignKey(Publisher)


class NumberOfPages(models.Model):
    arabic = models.PositiveIntegerField(default=0)
    roman = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.arabic) + ("roman: " + str(self.roman) if self.roman > 0 else "")


class Part(models.Model):
    part_name = models.CharField(max_length=20)
    part_number = models.PositiveIntegerField()
    number_of_parts = models.PositiveIntegerField(default=0)


class Format(models.Model):
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    def __str__(self):
        return str(self.width) + str(self.height)


class Cover(models.Model):
    type = models.CharField(max_length=50)
    is_with_wings = models.BooleanField(default=False)
    is_dust_jacket = models.BooleanField(default=False)

    def __str__(self):
        return self.type + ("with wings" if self.is_with_wings else "" + "with dust jacket" if self.is_dust_jacket else "")


class Category(models.Model):
    name = models.CharField(max_length=100)
    upper_category = models.ForeignKey("self", default=None, blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    part = models.OneToOneField(Part, default=None, null=True, blank=True)
    subtitle = models.CharField(max_length=200, default="", null=True, blank=True)
    isbn = models.BigIntegerField(default=0, unique=True)
    publisher = models.ForeignKey(Publisher, default=None)
    edition = models.OneToOneField(Edition, default=None)
    foreign_edition = models.OneToOneField(ForeignEdition, default=None, null=True, blank=True)
    series = models.ForeignKey(BookSeries, default=None, null=True, blank=True)
    number_of_pages = models.OneToOneField(NumberOfPages, default=None)
    format = models.OneToOneField(Format, default=None)
    weight = models.PositiveIntegerField(default=0)
    cover = models.OneToOneField(Cover, default=None)
    price_on_cover = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    categories = models.ManyToManyField(Category)
    cover_photo = models.ImageField(upload_to="covers", null=True)

    def __str__(self):
        return "{} {} {}".format(self.title, self.edition.number, self.author_set.all())


class Author(models.Model):
    book = models.ForeignKey(Book)
    author = models.ForeignKey(Person)
    is_editor = models.BooleanField(default=False)
    position = models.IntegerField()

    class Meta:
        ordering = ['position']
        unique_together = ('book', 'author', 'is_editor', 'position')

    def __str__(self):
        return self.author.getFullName() + (" (red.)" if self.is_editor else "")


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


class XeroBook(models.Model):
    book = models.OneToOneField(Book)
    xero_pages = models.IntegerField(default=0)
    actual_price = None
    actual_bind = None


    @property
    def xero_cards(self):
        return math.ceil(self.xero_pages/2)

    def set_actual_price(self, price):
        self.actual_price = price

    def set_actual_bind(self, bind):
        self.actual_bind = bind

    @property
    def bind_price(self):
        return self.actual_bind.get_bind_price(self.xero_cards)

    @property
    def xero_price(self):
        return round(Decimal(self.xero_pages * self.actual_price), 2)

    @property
    def xero_price_with_bind(self):
        return self.bind_price + self.xero_price


def create_xero_book(sender, **kwargs):
    if kwargs['created']:
        xero_book = XeroBook.objects.create(book=kwargs['instance'])

post_save.connect(create_xero_book, sender=Book)




