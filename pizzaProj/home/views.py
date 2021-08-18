from django.shortcuts import render, redirect
from django.views.decorators import csrf
from .models import *


def index(request):
    pizza = Pizza.objects.all()
    # order = Order.objects.all()
    order = Order.objects.order_by('-id')[:15]    # display the latest 15 orders

    context = {
        'title': 'Pizza App: Homepage',
        'pizzas': pizza,
        'orders': order,
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
