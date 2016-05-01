# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, render_to_response, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.mail import EmailMessage

from .models import *


COOKIES_ID ='walker_test3'
shop_name = u'Бродяга'


def _categories():
    return [brand for brand in Product.BRANDS]

def _products_in_cart(request):
    products_in_cart = len(CartElement.objects.filter(cart=Cart.objects.get(id=request.COOKIES.get(COOKIES_ID))))
    if products_in_cart > 0:
        return products_in_cart
    else: 
        return 0

def index(request):
    context = {
        'product_list': Product.objects.all(),
        'cookies_id': COOKIES_ID,
    }

    context['categories'] = _categories()
    context['products_in_cart'] = _products_in_cart(request)
    response = render(request, 'index.html', context)

    return response
 

def search(request):
    context = {
        'product_list': Product.objects.filter(name__contains=request.POST['search']),
        'categories': [brand for brand in Product.BRANDS]
    }
    context['products_in_cart'] = _products_in_cart(request)
    return render(request, 'index.html', context)


def product_list(request, brand):
    context = {
        'cat': str(brand),
        'product_list': Product.objects.filter(brand=brand),
        'categories': [brand for brand in Product.BRANDS]
    }
    return render(request, 'index.html', context)


def add_product_to_cart(request):
    context={}
    response = HttpResponseRedirect('/cart/')
    product_id = request.POST['product_id']
    if (request.COOKIES.get(COOKIES_ID)):
        cart = Cart.objects.get(
            id=request.COOKIES.get(COOKIES_ID)
        )
    else:
        cart = Cart.objects.create(
            total_amount=0
        )

    cart_id = cart.id
    cart_element = CartElement.objects.create(
        product=Product.objects.get(
                id=product_id 
            ),
        cart=Cart.objects.get(
                id=cart_id
            ),
        size=Size.objects.filter(
                size = request.POST['size']
            ).first()
        )
    size = Size.objects.filter(
        size = request.POST['size'],
        available=True
    ).first()

    size.available = False
    size.save()

    cart_element_id = cart_element.id
    response.set_cookie(
        key=COOKIES_ID, 
        value=str(cart_id),
        max_age=10000000
    ) # неделя

    available_sizes = Size.objects.filter(
        available=True,
        product=Product.objects.get(id=product_id)
    ).count()

    if (available_sizes == 0):
        product = Product.objects.get(
            id=product_id
        )

        product.available = False
        product.save()

    return response


def cart(request):
    context = {}
    cart_id = request.COOKIES.get(COOKIES_ID)

    cart_elements = CartElement.objects.filter(
        cart=cart_id
    )
    context['cart_elements'] = cart_elements
    context['products_in_cart'] = _products_in_cart(request)
    context['categories'] = [brand for brand in Product.BRANDS]
    
    return render(request, 'cart.html', context)    


def product(request, slug):
    target_product = Product.objects.get(slug=slug)
    context = {
        'product': target_product,
        'sizes': Size.objects.filter(product=target_product),
        'photos': Photo.objects.filter(product=target_product)
    }
    context['products_in_cart'] = _products_in_cart(request)
    context['categories'] = _categories()
    return render(request, 'product.html', context)


def checkout(request):
    context = {}
    context['products_in_cart'] = _products_in_cart(request)
    return render(request, 'checkout.html', context)


def create_order(request):
    response = HttpResponseRedirect('/order_status_form/')

    context = {
    }
    
    order = Order.objects.create(
        status=Order.OPEN,
        username=request.POST['username'],
        phone=request.POST['phone'],
        address=request.POST['address'],
        email=request.POST['email'],
        express_delivery=request.POST.get('express_delivery', False),
        cart=Cart.objects.get(
            id=request.COOKIES.get(COOKIES_ID)
        )
    )

    cart = Cart.objects.get(
        id=request.COOKIES.get(COOKIES_ID)
    )
    cart.closed = True
    cart.save()

    msg = EmailMessage(
        u'Заказ с интернет магазина - ' + shop_name,
        request.POST['username'] 
        + u''', ваш заказ принят. \nДля проверки статуса заказа перейдите по ссылке http://127.0.0.1:8000/order_status_form/ и воспользуйтесь следующими данными:\nИдентификатор заказа: ''' 
        + str(order.id) + '\n' 
        + u'Номер телефона: ' + str(request.POST['phone']), 
        to=['te7ris@mail.ru'])

    msg.send()

    response.delete_cookie(COOKIES_ID)

    return response


def order_status(request):
    context = {
        'order': Order.objects.get(
            id=request.POST['order_id'],
            phone=request.POST['phone']
        )
    }
    context['products_in_cart'] = _products_in_cart(request)

    return render(request, 'order_status.html', context)


def order_status_form(request):
    context = {
    }
    context['products_in_cart'] = _products_in_cart(request)

    return render(request, 'order_status_form.html', context)