from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Wishlist
from .serializers import WishlistSerializer,WishlistCreateSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class WishlistAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get Wishlist",
        responses={200: WishlistSerializer(many=True)}
    )
    def get(self, request):
        wishlist_items = (
            Wishlist.objects
            .filter(user=request.user)
            .select_related("product", "product__category")
            .order_by("-id")
        )

        serializer = WishlistSerializer(wishlist_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Add to Wishlist",
        request_body=WishlistCreateSerializer,
        responses={201: WishlistSerializer}
    )
    def post(self, request):
        product_id = request.data.get("product")

        if not product_id:
            return Response(
                {"error": "Product ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Wishlist.objects.filter(user=request.user, product_id=product_id).exists():
            return Response(
                {"message": "Already in wishlist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        wishlist_item = Wishlist.objects.create(
            user=request.user,
            product_id=product_id
        )

        serializer = WishlistSerializer(wishlist_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class WishlistDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Remove from Wishlist",
        manual_parameters=[
            openapi.Parameter(
                "product_id",
                openapi.IN_PATH,
                description="Product ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={204: "Deleted", 404: "Not found"}
    )
    def delete(self, request, product_id):
        try:
            item = Wishlist.objects.get(user=request.user, product_id=product_id)
            item.delete()

            return Response(
                {"message": "Removed from wishlist"},
                status=status.HTTP_204_NO_CONTENT
            )

        except Wishlist.DoesNotExist:
            return Response(
                {"error": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )