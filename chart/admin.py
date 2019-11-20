from django.contrib import admin

# Register your models here.
from . models import Company, StockSeries

admin.site.register(Company)
admin.site.register(StockSeries)