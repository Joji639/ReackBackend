from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from .models import Products, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Products.objects.all()

        category = self.request.query_params.get("category")
        bestseller = self.request.query_params.get("bestseller")

        if category:
            queryset = queryset.filter(category__name__iexact=category)

        if bestseller is not None:
            if bestseller.lower() == "true":
                queryset = queryset.filter(bestseller=True)
            elif bestseller.lower() == "false":
                queryset = queryset.filter(bestseller=False)

        return queryset


class ProductDetailView(RetrieveAPIView):
    queryset = Products.objects.select_related("category").all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]