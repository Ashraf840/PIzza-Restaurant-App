from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from restaurant_staff.decorators import *


# Main dashboard for the restaurant-staffs only [HomePage]
@login_required(login_url='userAuth:login')
@stop_regular_customer
def index(request):
    context = {}
    return render(request, 'restaurant_staff/index.html', context)