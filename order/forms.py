from django.db.models import fields
from .models.products import Product
from .models.orders import Order, OrderItems

from django import forms
from django.forms.models import BaseInlineFormSet


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'size', 'image']

class OrderItemsForm(forms.ModelForm):
    class Meta:
        model = OrderItems
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'