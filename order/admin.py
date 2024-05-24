from django.contrib import admin
from order.models.products import Product
from order.forms import ProductForm, OrderForm
from .models.orders import Order, OrderItems



class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    ordering = ['id']

class OrderItemsInline(admin.StackedInline):
    model = OrderItems
    fields = ['id','order','product', 'quantity', 'changes']  

class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    list_display = ('id','user','cpf','status', 'created_at', 'updated_at')
    inlines = [OrderItemsInline,]
    list_filter = ('user','cpf','status',)
    list_per_page = 25
    

admin.site.register(Product, ProductAdmin)
#admin.site.register(OrderItems, OrderItemsAdmin)
admin.site.register(Order, OrderAdmin)
