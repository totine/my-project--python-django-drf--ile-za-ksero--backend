from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(BindRange)
admin.site.register(Bind)
admin.site.register(XeroBaseBookCalc)
admin.site.register(XeroBookCalc)
admin.site.register(XeroSimpleCalc)
admin.site.register(XeroList)

