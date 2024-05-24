from order.models import Product

class ListProductsUseCase:
    def execute(self, query_params):
        queryset = Product.objects.using('default').all()
        category = query_params.get('category', None)

        if category:
            queryset = queryset.filter(category=category)

        return queryset
