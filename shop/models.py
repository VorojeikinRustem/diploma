# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Product(models.Model):
    ASICS = 'asics'
    JORDAN = 'jordan'
    NIKE = 'nike'
    NEW_BALANCE = 'new_balance'
    BRANDS = (
        (ASICS, 'Asics'),
        (JORDAN, 'Jordan'),
        (NIKE, 'Nike'),
        (NEW_BALANCE, 'New Balance'),
    )
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    
    price = models.PositiveIntegerField()
    brand = models.CharField(
        max_length = 15,
        choices = BRANDS, 
        default = ASICS
    )
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    SIZES = ((i, str(i)) for i in range(32,48))
    size = models.PositiveIntegerField(
        choices = SIZES,
        default = 45 
    )
    available = models.BooleanField(default=True)
    product = models.ForeignKey(Product)

    def __str__(self):
        return str(self.size)


class Photo(models.Model):
    img = models.ImageField(
        upload_to='images/sneakers'
    )

    product = models.ForeignKey(Product)
    
    def __str__(self):
        return str(self.id)
        

class Cart(models.Model):
    total_amount = models.FloatField()  
    closed = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)


class CartElement(models.Model):
    cart = models.ForeignKey(Cart)
    product = models.ForeignKey(Product)
    size = models.ForeignKey(Size)

    def __str__(self):
        return str(self.id)


@python_2_unicode_compatible
class Order(models.Model):
    OPEN = 'open'
    PREPARED = 'prepared'
    DELIVER = 'deliver'
    COMPLETED = 'completed'
    CANCEL = 'cancel'
    STATUSES = (
        (OPEN, u'Принят'),
        (PREPARED, u'Оформление'),
        (CANCEL, u'Отменен'),
        (DELIVER, u'Доставляется'),
        (COMPLETED, u'Доставлен'),
    )
    status = models.CharField(
        max_length=20,
        choices = STATUSES,
        default = OPEN
    )
    username = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=254)
    email = models.EmailField(max_length=100)
    express_delivery = models.BooleanField()
    checkout_datetime = models.DateTimeField(auto_now_add=True)

    cart = models.OneToOneField(Cart)

    def __str__(self):
        return str(self.id) + '. ' + str(self.phone)

