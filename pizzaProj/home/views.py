from django.core import paginator
from django.shortcuts import render, redirect
from django.views.decorators import csrf
from .models import *
from django.core.paginator import Paginator


def index(request):
    pizza = Pizza.objects.all()
    # order = Order.objects.all()
    # order = Order.objects.order_by('-id')[:10]    # display the latest 15 orders
    order = Order.objects.order_by('-id')

    total_order_num = len(order)

    order_paginator = Paginator(order, 5)
    page = request.GET.get('page')
    paginated_order_list_query = order_paginator.get_page(page)

    context = {
        'title': 'Pizza App: Homepage',
        'pizzas': pizza,
        'total_order_num': total_order_num,
        'orders': paginated_order_list_query,
    }
    return render(request, 'home/index.html', context)


def order(request, order_id):
    order = Order.objects.filter(order_id=order_id).first()

    # If no such order with this order_id is found, redirect user to the home-page.
    if order is None:
        return redirect('homeApplication:homepage')

    context = {
        'title': 'Pizza App: Order Page',
        'order': order,
    }
    return render(request, 'home/order.html', context)



# An API View is created inside this "pizzaProj/home/api/views.py" file.
