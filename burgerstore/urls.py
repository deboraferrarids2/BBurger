"""
URL configuration for burgerstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from user_auth.views import UserViewSet, signin
from order.views import ProductViewSet, OrderViewSet, OrderItemsViewSet
from payment.views import CheckoutViewset, TransactionWebhookView


router = routers.DefaultRouter()

router.register('user', UserViewSet, basename='user')
router.register('products', ProductViewSet)
router.register('order', OrderViewSet, basename='order')
router.register('items', OrderItemsViewSet)
router.register('payment', CheckoutViewset)




urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('signin/', signin, name='signin'),
    #path('user/<int:pk>/delete/', delete_user, name='delete_user'),
    path('webhook/', TransactionWebhookView.as_view(), name='webhook'),
    path('user/', UserViewSet.create, name='user'),
    path('order_create/', OrderViewSet.create, name='order_create'),
    path('order_retrieve/<int:pk>/', OrderViewSet.retrieve, name='order_retrieve'),
    path('items_create/', OrderItemsViewSet.create, name='items_create'),


]

