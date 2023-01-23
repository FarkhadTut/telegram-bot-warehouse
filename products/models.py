from doctest import set_unittest_reportflags
from pyexpat import model
from urllib import response
from django.db import models
from numpy import blackman
from survey.models import Poll

# Create your models here.


class Type(models.Model):
    WAREHOUSES = (
        ('raw', 'Xom ashyo'),
        ('ready_prod', 'Tayyor maxsulot'),
    )
    ru = models.TextField(max_length=4096, blank=True)
    uz = models.TextField(max_length=4096, blank=False)
    poll = models.ForeignKey(to=Poll, on_delete=models.SET_NULL, null=True)
    deleted = models.BooleanField(default=False)
    warehouse = models.CharField(choices=WAREHOUSES, max_length=20, default='raw', null=False, blank=False)
    def __str__(self):
        return self.uz

class Product(models.Model):
    ru = models.TextField(max_length=4096, blank=True)
    uz = models.TextField(max_length=4096, blank=False)
    type = models.ForeignKey(to=Type, on_delete=models.SET_NULL, null=True)
    deleted = models.BooleanField(default=False)
    # identifier = models.ForeignKey(to=Identifier, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.uz

class Identifier(models.Model):
    ru = models.TextField(max_length=4096, blank=True)
    uz = models.TextField(max_length=4096, blank=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.uz



class Record(models.Model):
    ACTIONS = (
        ('kirim', 'Kirim'),
        ('chiqim', 'Chiqim'),
    )

    UNITS = (
        ('korobka', 'Korobka'),
        ('qop', 'Qop'),
    )   

    response_id = models.IntegerField(null=False, blank=False)
    question_id = models.IntegerField(null=False, blank=False)
    response_type = models.CharField(max_length=512, null=False, blank=False)
    response_id_source = models.CharField(max_length=512, null=False, blank=True)


