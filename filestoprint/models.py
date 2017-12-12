from django.db import models


class File(models.Model):
    path = models.FilePathField()
