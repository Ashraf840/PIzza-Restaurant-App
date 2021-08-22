from django import forms
from django.db.models import fields
from home.models import *


class OrderStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']



class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = "__all__"