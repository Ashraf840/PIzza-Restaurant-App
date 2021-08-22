from django.shortcuts import render, redirect
from django.views.decorators import csrf
from .models import *
from django.core.paginator import Paginator


def index(request):
    # Pizza Query
    pizza = Pizza.objects.all()

    total_pizza_num = len(pizza)

    pizza_paginator = Paginator(pizza, 4)
    pizza_page = request.GET.get('page')
    paginated_pizza_list_query = pizza_paginator.get_page(pizza_page)


    # Order Query
    order = Order.objects.order_by('-id')   # display the latest orders

    total_order_num = len(order)

    order_paginator = Paginator(order, 5)
    order_page = request.GET.get('page')
    paginated_order_list_query = order_paginator.get_page(order_page)

    context = {
        'title': 'Pizza App: Homepage',

        'pizzas': paginated_pizza_list_query,
        'total_pizza_num': total_pizza_num,

        'orders': paginated_order_list_query,
        'total_order_num': total_order_num,
    }
    return render(request, 'home/index.html', context)

# An API View is created inside this "pizzaProj/home/api/views.py" file.


def order(request, order_id):
    order = Order.objects.filter(order_id=order_id).first()

    # If no such order with this order_id is found, redirect user to the home-page.
    if order is None:
        return redirect('homeApplication:homepage')

    context = {
        'title': 'Pizza App: Order Status Page',
        'order': order,
    }
    return render(request, 'home/order.html', context)




# Oder-List page
def order_list(request):
    # Order Query
    order = Order.objects.order_by('-id')   # display the latest orders

    total_order_num = len(order)

    order_paginator = Paginator(order, 5)
    order_page = request.GET.get('page')
    paginated_order_list_query = order_paginator.get_page(order_page)

    context = {
        'title': 'Orders List',

        'orders': paginated_order_list_query,
        'total_order_num': total_order_num,
    }

    return render(request, 'home/order_list.html', context)