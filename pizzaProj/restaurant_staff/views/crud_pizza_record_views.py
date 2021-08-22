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


# Update pizza record (for restaurant-staffs)
def updatePizza(request, pizza_id):
    pizza = Pizza.objects.filter(pk=pizza_id).first()
    form = PizzaForm(instance=pizza)

    if request.method == 'POST':
        form = PizzaForm(request.POST, request.FILES, instance=pizza)   # REQUIRED since an image is also getting uploaded using this form; instance will only update that specific record
        if form.is_valid():
            form.save()
            return redirect('restaurantStaffApplication:pizzaRecords')    # redirect to the pizza-record page

    context = {
        'title': 'Restaurant Staffs: Update Pizza Record',
        'pizza': pizza,
        'pizzaForm': form,
    }
    return render(request, 'restaurant_staff/update_pizza_record.html', context)


# Delete pizza record (for restaurant-staffs)
def deletePizza(request, pizza_id):
    pizza = Pizza.objects.filter(pk=pizza_id).first()

    if request.method == 'POST':
        pizza.delete()
        return redirect('restaurantStaffApplication:pizzaRecords')    # redirect to the pizza-record page

    context = {
        'title': 'Restaurant Staffs: Delete Pizza Record',
        'pizza': pizza,
    }
    return render(request, 'restaurant_staff/delete_pizza_record.html', context)
