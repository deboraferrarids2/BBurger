from order.models import Order
from rest_framework import status
from django.db.models import Case, When, IntegerField, Value
from order.serializers.orders import *

class ListOrdersUseCase:
    def execute(self, request):
        status = request.query_params.get('status', None)
        user = request.user

        # Query the Order model directly
        queryset = Order.objects.all()

        if user.is_authenticated:
            if not user.is_staff:
                queryset = queryset.filter(user=user)
        else:
            queryset = queryset.filter(session_token=request.query_params.get('session'))

        if status:
            queryset = queryset.filter(status=status)

        # Apply custom ordering
        queryset = self.apply_custom_ordering(queryset)

        return queryset

    def apply_custom_ordering(self, queryset):
        queryset = queryset.annotate(
            custom_order=Case(
                When(status='pronto', then=Value(0)),
                When(status='em preparacao', then=Value(1)),
                When(status='recebido', then=Value(2)),
                default=Value(3),  # Add default value for other statuses
                output_field=IntegerField(),
            )
        ).filter(custom_order__lte=2)  # Keep only objects with status 0, 1, or 2

        return queryset
