from django.db import models


class Headnav(models.Model):
    name = models.CharField(max_length=200, verbose_name='Bosh sahifa ismi:')
    title = models.CharField(max_length=150, blank=True, null=True, verbose_name='azgina malumot:')


class Trend(models.Model):
    name = models.CharField(max_length=70, verbose_name='Kiym modeli:')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Narxi:')
    img = models.ImageField(upload_to='home/', verbose_name='Rasm:')

    def __str__(self):
        return self.name
    

class Box(models.Model):
    name = models.CharField(max_length=70, verbose_name='Kiym modeli:')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Narxi:')
    img = models.ImageField(upload_to='home/', verbose_name='Rasm:')


    def  __str__(self):
        return self.name
    