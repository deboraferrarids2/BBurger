from rest_framework.permissions import AllowAny
from user_auth.mixed_views import MixedPermissionModelViewSet
from order.models.products import Product
from order.serializers.products import *
from order.use_cases.products import ListProductsUseCase

class ProductViewSet(MixedPermissionModelViewSet):

    queryset = Product.objects.using('default').all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    
    
    def get_queryset(self):
        list_products_use_case = ListProductsUseCase()
        return list_products_use_case.execute(self.request.query_params)
