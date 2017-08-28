from django.db import models

# Create your models here.


class Author(models.Model):
    firstname = models.CharField(max_length=50)
    secondname = models.CharField(max_length=50, default="")
    surname = models.CharField(max_length=50)


class Book(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, default="")
    year_of_publish = models.IntegerField()


class BookAuthor(models.Model):
    book = models.ForeignKey(Book)
    author = models.ForeignKey(Author)
    is_editor = models.BooleanField(default=False)
    position = models.IntegerField()

    class Meta:
        ordering = ['position']
        unique_together = ('book', 'author', 'is_editor', 'position')