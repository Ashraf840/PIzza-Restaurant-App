from django.urls import path, include
from .views import order_status_update_views, crud_pizza_record_views, views

app_name = 'restaurantStaffApp'

urlpatterns = [
    # For Restaurant Staffs Only

    # Order Status Update - Related
    path('', views.index, name='home_restaurant_staffs'),
    path('order-list/', order_status_update_views.restaurant_order_status_list, name='restaurantBackendOrderStatus'),
    path('order-status-update/<str:order_id>/', order_status_update_views.restaurant_order_status_update, name='orderStatusUpdate'),

    # Pizza Record CRUD - Related
    path('pizza/pizza-records/', crud_pizza_record_views.pizzaList, name='pizzaRecords'),
    path('pizza/create-pizza-record/', crud_pizza_record_views.createPizza, name='createPizzaRecord'),
    path('pizza/update-pizza-record/<str:pizza_id>/', crud_pizza_record_views.updatePizza, name='updatePizzaRecord'),
    path('pizza/delete-pizza-record/<str:pizza_id>/', crud_pizza_record_views.deletePizza, name='deletePizzaRecord'),
]