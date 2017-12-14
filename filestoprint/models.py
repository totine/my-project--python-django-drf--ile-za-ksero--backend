from django.db import models
from bookbase.settings import MEDIA_ROOT
import PyPDF2


class FileToPrint(models.Model):
    path = models.FilePathField(path=MEDIA_ROOT+'files-to-print')

