from django.shortcuts import render, redirect
from home.models import *
from restaurant_staff.forms import *



# Shows all the pizzas (for restaurant-staffs)
def pizzaList(request):
    pizzas = Pizza.objects.all()
    total_pizza_num = len(pizzas)

    context = {
        'title': 'Restaurant Staffs: Pizza List',

        'pizzas': pizzas,
        'total_pizza_num': total_pizza_num,
    }
    return render(request, 'restaurant_staff/pizza_list.html', context)


# Create new pizza record (for restaurant-staffs)
def createPizza(request):
    form = PizzaForm()

    if request.method == 'POST':
        form = PizzaForm(request.POST, request.FILES)   # REQUIRED since an image is also getting uploaded using this form
        if form.is_valid():
            form.save()
            return redirect(request.get_full_path())    # redirect to the same page

    context = {
        'title': 'Restaurant Staffs: New Pizza Record',
        'pizzaForm': form,
    }
    return render(request, 'restaurant_staff/create_pizza_record.html', context)