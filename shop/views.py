# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, render_to_response, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.mail import EmailMessage

from .models import *


COOKIES_ID = 'shop'
PHONE_NUMBER = 79781234567
SHOP_NAME = 'Crimea Sneakers'

 
def _categories():
    return [brand for brand in Product.BRANDS]


def _current_category(brand):
    return brand


def _products_in_cart(request):
    if (request.COOKIES.get(COOKIES_ID, 0) != 0):
        products_in_cart = len(CartElement.objects.filter(cart=Cart.objects.get(id=request.COOKIES.get(COOKIES_ID, 0))))
    else: 
        products_in_cart = 0
    return products_in_cart


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
        'product_list': Product.objects.filter(brand=brand),
        'categories': [brand for brand in Product.BRANDS]
    }
    context['current_category'] = _current_category(brand)
    context['products_in_cart'] = _products_in_cart(request)
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
    cart.total_amount += Product.objects.get(id=product_id).price
    cart.save()

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
    context['total'] = sum([i.product.price for i in cart_elements])
    
    return render(request, 'cart.html', context)    


def product(request, brand, slug):
    target_product = Product.objects.get(brand=brand, slug=slug)
    context = {
        'product': target_product,
        'sizes': Size.objects.filter(product=target_product),
        'photos': Photo.objects.filter(product=target_product)
    }
    context['products_in_cart'] = _products_in_cart(request)
    context['categories'] = _categories()
    context['breadcrumb_brand'] = target_product.brand
    context['breadcrumb_slug'] = target_product.slug
    context['current_category'] = _current_category(brand)
    return render(request, 'product.html', context)


def checkout(request):
    context = {}
    context['products_in_cart'] = _products_in_cart(request)
    return render(request, 'checkout.html', context)


def create_order(request):
    # response = HttpResponseRedirect('/order_status_form/')

    context = {
    }
    context['products_in_cart'] = _products_in_cart(request)
    context['order_accepted'] = True

    response = render(request, 'order_status_form.html', context)

    if (request.POST['username'] == '' or request.POST['phone'] == '' or request.POST['address'] == '' or request.POST['email'] == ''):
        context['empty_form'] = True
        return render(request, 'checkout.html', context)

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

    message = unicode(request.POST['username']) + u', добрый день.\nДля проверки статуса заказа воспользуйтесь следующими данными: \nНомер заказа: ' + unicode(order.id) + u'\nНомер телефона: ' + unicode(request.POST['phone']) + u'''
        \nСтатусы заказа:
        Принят - заказ зарегестрирован. Возможно с вами свяжется администратор по телефону или электронной почты в случае возникших вопросов.
        Оформление - сбор заказанных товаров. Проверка товаров на наличие дефекты.
        Доставляется - ваш заказ доставляется курьером. Возможен звонок вам на телефон для уточнения места получения вами заказа.
        Доставлен - заказ доставлен покупателю. Если это ваш заказ и вы не получили его, то срочно сообщити об этом нам.
        Отменен - по какой-либо причине заказ был отменен.
        '''    

    cart = Cart.objects.get(
        id=request.COOKIES.get(COOKIES_ID)
    )

    if (request.POST['express_delivery']):
        message + u'''\nВаш заказ для нас является приоритетным, так как вы выбрали срочную доставку.\nТовар будет доставлен в течении 5 часов.'''
        cart.total_amount += 500
    else:
        message + u'\nТовар будет доставлен в течении 3 дней'

    cart.closed = True
    cart.save()

    msg = EmailMessage(
        u'Заказ с интернет магазина - ' + SHOP_NAME,
        message + u'\nЗа дополнительной информацией обращайтесь по номеру: ' + str(PHONE_NUMBER) + u'\nСтоимость заказа: ' + str(cart.total_amount) + u' рублей.', 
        to=[request.POST['email']])

    msg.send()

    # response.delete_cookie(COOKIES_ID)
    response.delete_cookie(COOKIES_ID)

    # return response
    return response

def order_status(request):
    
    if (request.POST['phone'] == '' or request.POST['order_id'] == ''):
        return redirect('/order_status_form/')
    
    try:
        order = Order.objects.get(
            id=request.POST['order_id'],
            phone=request.POST['phone']
        )
    except Order.DoesNotExist:
        context = {
            'order_does_not_exist': True,
            'order_id': request.POST['order_id'],
            'order_phone': request.POST['phone']
        }
        context['products_in_cart'] = _products_in_cart(request)
        return render(request, 'order_status_form.html', context)

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