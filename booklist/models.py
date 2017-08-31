from django.db import models
from django.db.models.signals import post_save


class Person(models.Model):
    firstname = models.CharField(max_length=50)
    secondname = models.CharField(max_length=50, default="")
    surname = models.CharField(max_length=50)


class Country(models.Model):
    name = models.CharField(max_length=50)


class City(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country)


class Publisher(models.Model):
    full_name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=30, default=None, null=True)
    city = models.ForeignKey(City)


class Edition(models.Model):
    number = models.PositiveIntegerField(default=1)
    year = models.PositiveIntegerField()
    comment = models.CharField(max_length=50, default=None)


class Language(models.Model):
    name = models.CharField(max_length=50)


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


class Part(models.Model):
    part_name = models.CharField(max_length=20)
    part_number = models.PositiveIntegerField()
    number_of_parts = models.PositiveIntegerField(default=0)


class Format(models.Model):
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()


class Cover(models.Model):
    type = models.CharField(max_length=50)
    is_with_wings = models.BooleanField(default=False)
    is_dust_jacket = models.BooleanField(default=False)


class Book(models.Model):
    title = models.CharField(max_length=200)
    part = models.OneToOneField(Part, default=None)
    subtitle = models.CharField(max_length=200, default="")
    isbn = models.PositiveIntegerField(default=0, unique=True)
    publisher = models.ForeignKey(Publisher, default=None)
    edition = models.OneToOneField(Edition, default=None)
    foreign_edition = models.OneToOneField(ForeignEdition, default=None)
    series = models.ForeignKey(BookSeries, default=None)
    number_of_pages = models.OneToOneField(NumberOfPages, default=None)
    format = models.OneToOneField(Format, default=None)
    cover = models.OneToOneField(Cover, default=None)
    price_on_cover = models.DecimalField(max_digits=6, decimal_places=2, default=0)


class Author(models.Model):
    book = models.ForeignKey(Book)
    author = models.ForeignKey(Person)
    is_editor = models.BooleanField(default=False)
    position = models.IntegerField()

    class Meta:
        ordering = ['position']
        unique_together = ('book', 'author', 'is_editor', 'position')


class XeroBook(models.Model):
    book = models.OneToOneField(Book)
    xero_pages = models.IntegerField()


def create_xero_book(sender, **kwargs):
    if kwargs['created']:
        xero_book = XeroBook.objects.create(book = kwargs['instance'])

post_save.connect(create_xero_book, sender=Book)




