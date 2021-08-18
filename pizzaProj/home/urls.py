from django.urls import path, include
from . import views

app_name = 'homeApp'

urlpatterns = [
    path('', views.index, name='homepage'),
    path('order/<str:order_id>', views.order, name='order'),
    path('api/', include('home.api.urls')),
]