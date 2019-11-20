from django.db import models

# Create your models here.

class Company(models.Model) :
    
    stock_id = models.CharField(max_length=6, help_text='the Stock ID of a Company', primary_key=True)
    company_name = models.CharField(max_length=25, help_text='the Name of a Company')
        
    def save_data(self) :
        self.save(using=self._meta.app_label)
    
    def __str__(self) :
        return "{} {}".format(self.stock_id, self.company_name)
    class Meta :
        app_label = 'chart'

class StockSeries(models.Model) :

    ofWhich = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, unique=None)
    time = models.DateField(blank=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    open = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)

    def save_data(self) :
        self.save(using=self._meta.app_label)

    def __str__(self) :
        return "{} {}".format(self.time, self.ofWhich.company_name)

    class Meta : 
        ordering = ['ofWhich']
        verbose_name = 'StockSeries'
        app_label = 'chart'