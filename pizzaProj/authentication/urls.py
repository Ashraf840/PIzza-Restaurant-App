from django.urls import path, include
from . import views

app_name = 'authApp'

urlpatterns = [
    path('user_login/', views.userLogin, name='login'),
    path('user_signup/', views.userReg, name='registration'),
    path('user_logout/', views.userLogout, name='logout'),
]