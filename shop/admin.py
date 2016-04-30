# -*- coding: UTF-8 -*-

from django.contrib import admin

from .models import Product, Cart, CartElement, Size, Order, Photo


class SizeInline(admin.StackedInline):
    model = Size
    extra = 3

class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 4

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'price')
    inlines = [SizeInline, PhotoInline]


class CartElementAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'size')


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_amount')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone', 'address', 'email', 'status', 'express_delivery', 'checkout_datetime', 'cart')


admin.site.register(Product, ProductAdmin)
admin.site.register(CartElement, CartElementAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order)

