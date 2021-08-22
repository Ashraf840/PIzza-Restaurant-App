from django.shortcuts import render, redirect
from home.models import *
from restaurant_staff.forms import *


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



def restaurant_order_status_update(request, order_id):
    order = Order.objects.filter(order_id=order_id).first()

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
    }
    return render(request, 'restaurant_staff/order_stat_updation.html', context)