from django.shortcuts import render, redirect
from django.views.decorators import csrf
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .decorators import *


# Main dashboard for regular restaurant-customers
@login_required(login_url='userAuth:login')
@stop_restaurant_staff
def index(request):
    try:
        user = request.user     # This will only render the company_name of the user, for which the regular-customer don't have
        user = user.get_full_name()     # Get the full-name of the logged-in user
    # Optional to use the 'except'
    except:
        user = 'Anonymous User'

    # Pizza Query
    pizza = Pizza.objects.all()

    total_pizza_num = len(pizza)

    pizza_paginator = Paginator(pizza, 4)
    pizza_page = request.GET.get('page')
    paginated_pizza_list_query = pizza_paginator.get_page(pizza_page)


    context = {
        'title': 'Pizza App: Homepage',
        
        'user': user,

        'pizzas': paginated_pizza_list_query,
        'total_pizza_num': total_pizza_num,
    }
    return render(request, 'home/index.html', context)

# An API View is created inside this "pizzaProj/home/api/views.py" file.



# Sepcific oder detail page (for Regular Frontend Customers) [Websocket Enabled Page]
@login_required(login_url='userAuth:login')
@stop_restaurant_staff
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




# Oder-List page (for Regular Frontend Customers)
@login_required(login_url='userAuth:login')
@stop_restaurant_staff
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



def error_404_view(request, exception):
    return render(request, '404_page_not_found.html')