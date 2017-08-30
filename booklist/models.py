from django.db import models

# Create your models here.


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
    name = models.CharField(max_length=50)
    city = models.ForeignKey(City)


class Edition(models.Model):
    number = models.PositiveIntegerField(default=1)
    year = models.PositiveIntegerField()
    comment = models.CharField(max_length=50)


class ForeignEdition(models.Model):
    number = models.PositiveIntegerField(default=1)
    year = models.PositiveIntegerField()
    publisher = models.ForeignKey(Publisher)


class BookSeries(models.Model):
    name = models.CharField(max_length=100)
    publisher = models.ForeignKey(Publisher)


class Book(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, default="")
    isbn = models.PositiveIntegerField(default=0)
    edition = models.OneToOneField(Edition)
    foreign_edition = models.OneToOneField(ForeignEdition, default=None)
    series = models.ForeignKey(BookSeries, default=None)


class Author(models.Model):
    book = models.ForeignKey(Book)
    author = models.ForeignKey(Person)
    is_editor = models.BooleanField(default=False)
    position = models.IntegerField()

    class Meta:
        ordering = ['position']
        unique_together = ('book', 'author', 'is_editor', 'position')



