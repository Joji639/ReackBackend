from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from paymentpage.models import Order
from .serializers import OrderCardSerializer


class OrderPageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)\
            .prefetch_related("items")\
            .order_by("-created_at")

        response_data = []

        for order in orders:
            for item in order.items.all():
                response_data.append({
                    "order_id": order.id,
                    "status": order.status,
                    "created_at": order.created_at,

                    "product_name": item.product.title,
                    "image": item.product.img if item.product.img else None,
                    "quantity": item.quantity,
                    "price": item.price,
                })

        serializer = OrderCardSerializer(response_data, many=True)
        return Response(serializer.data)