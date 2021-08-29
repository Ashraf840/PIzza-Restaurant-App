from django.shortcuts import render, redirect
from home.models import *
from restaurant_staff.forms import *
from django.contrib.auth.decorators import login_required
from restaurant_staff.decorators import *


# All orders-list for restaurant-staffs
@login_required(login_url='userAuth:login')
@stop_regular_customer
def restaurant_order_status_list(request):
    # Order Query
    order = Order.objects.order_by('-id')   # display the latest orders
    total_order_num = len(order)

    context = {
        'title': 'Restaurant Staff: Orders List',
        'orders': order,
        'total_order_num': total_order_num,
    }
    return render(request, 'restaurant_staff/order_stat_list.html', context)


# Update order-status page for 
@login_required(login_url='userAuth:login')
@stop_regular_customer
def restaurant_order_status_update(request, order_id):
    order = Order.objects.filter(order_id=order_id).first()

    order_user_full_name = order.user.first_name + ' ' + order.user.last_name
    # print(order.user.first_name)
    # print('%s %s' % (order.user.first_name, order.user.last_name))

    form = OrderStatusUpdateForm(instance=order)

    # If no such order with this order_id is found, redirect user to the home-page.
    if order is None:
        return redirect('restaurantStaffApplication:restaurantBackendOrderStatus')

    if request.method == 'POST':
        form = OrderStatusUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect(request.get_full_path())    # redirect to the same page

    context = {
        'title': 'Restaurant Staff: Order Update',
        'order': order,
        'orderForm': form,
        'user_full_name': order_user_full_name,
    }
    return render(request, 'restaurant_staff/order_stat_updation.html', context)