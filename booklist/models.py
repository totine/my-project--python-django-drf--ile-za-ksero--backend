from django.db import models

# Create your models here.


class Author(models.Model):
    firstname = models.CharField(max_length=50)
    secondname = models.CharField(max_length=50, default="")
    surname = models.CharField(max_length=50)


class Book(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, default="")
    isbn = models.IntegerField()


class BookAuthor(models.Model):
    book = models.ForeignKey(Book)
    author = models.ForeignKey(Author)
    is_editor = models.BooleanField(default=False)
    position = models.IntegerField()

    class Meta:
        ordering = ['position']
        unique_together = ('book', 'author', 'is_editor', 'position')


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


class BookSeries(models.Model):
    name = models.CharField(max_length=100)
    publisher = models.ForeignKey(Publisher)
