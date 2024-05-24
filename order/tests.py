from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test import RequestFactory
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import APIClient
from .models import Order, Product, OrderItems
from .serializers import OrderSerializer
from user_auth.models import BaseUser, Cpf
from .views import OrderViewSet, OrderItemsViewSet

import random
import string

User = get_user_model()

class CreateOrderTests(APITestCase):
    def setUp(self):

        self.user = self.get_or_create_user()

        # Generate a random suffix for the product name
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # Create default products for testing
        self.default_product_1 = Product.objects.create(
            name=f'Default Product {random_suffix}',
            category='bebida',
            description=f'A default product for testing {random_suffix}',
            size='medio',
            amount=1000
        )

        self.default_product_2 = Product.objects.create(
            name=f'Default Product {random_suffix}',
            category='bebida',
            description=f'A default product for testing {random_suffix}',
            size='medio',
            amount=2000 
        )

    def get_or_create_user(self):
        user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': f'testuser_{"".join(random.choices(string.ascii_lowercase, k=8))}@example.com',
        }

        response = self.client.post(reverse('user'), user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email=user_data['email'])

        return user

    def authenticate_user(self, user):
        response = self.client.post(reverse('signin'), {'email': user.email, 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data.get('access', '')

    def test_create_order_authenticated_with_null_cpf(self):
        user = self.get_or_create_user()

        self.client = APIClient()
        self.client.force_authenticate(user=user)
        
        # Create a Request object
        factory = APIRequestFactory()
        request = factory.post(reverse('order_create'), {'cpf': ''})

        # Pass the Request object to the view set
        response = OrderViewSet.as_view({'post': 'create'})(request)

        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

    def test_create_order_authenticated_with_non_null_cpf(self):
        user = self.get_or_create_user()
        self.client.force_authenticate(user=user)

        # Create a Request object
        factory = APIRequestFactory()
        request = factory.post(reverse('order_create'))
        
        # Pass the Request object to the view set
        response = OrderViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_items_authenticated(self):
        user = self.get_or_create_user()
        
        self.client = APIClient()

        self.client.force_authenticate(user=user)

        # Create an order with order items
        order = Order.objects.create(user=user)

        # Create order items using a POST request to the 'items_create' endpoint
        factory = RequestFactory()
        request = factory.post(reverse('items_create'), {
            'order': order.id,
            'product': self.default_product_1.id,
            'quantity': 2,
            'changes': 'Sem sal'
        })
        response_item1 = OrderItemsViewSet.as_view({'post': 'create'})(request)

        request = factory.post(reverse('items_create'), {
            'order': order.id,
            'product': self.default_product_2.id,
            'quantity': 1,
            'changes': ''
        })
        response_item2 = OrderItemsViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response_item1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_item2.status_code, status.HTTP_201_CREATED)

    def test_create_order_items_unauthenticated_with_session(self):
        # Create an order initially
        order = Order.objects.create()
        session_token = order.session_token

        # Create a RequestFactory instance
        request_factory = RequestFactory()

        # Create order items using a POST request to the 'items_create' endpoint
        request_item1 = request_factory.post(reverse('items_create'), {
            'order': order.id,
            'product': self.default_product_1.id,
            'quantity': 2,
            'changes': 'Sem sal'
        }, HTTP_SESSION_TOKEN=session_token)

        response_item1 = OrderItemsViewSet.as_view({'post': 'create'})(request_item1)

        request_item2 = request_factory.post(reverse('items_create'), {
            'order': order.id,
            'product': self.default_product_2.id,
            'quantity': 1,
            'changes': ''
        }, HTTP_SESSION_TOKEN=session_token)

        response_item2 = OrderItemsViewSet.as_view({'post': 'create'})(request_item2)

        # Check the responses for successful creation
        self.assertEqual(response_item1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_item2.status_code, status.HTTP_201_CREATED)

        # Retrieve the order and check its details
        request_retrieve = request_factory.get(reverse('order_retrieve', args=[order.id]))
        response_retrieve = OrderViewSet.as_view({'get': 'retrieve'})(request_retrieve, pk=order.id)

        self.assertEqual(response_retrieve.status_code, status.HTTP_200_OK)
