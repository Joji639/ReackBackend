from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .permissions import IsAdminUser
from .serializers import *

from allproducts.models import Products
from User.models import UserModel
from paymentpage.models import Order
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi





class AdminUserListView(ListAPIView):
    queryset = UserModel.objects.all().order_by("-id")
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]


class ToggleUserStatusView(APIView):
    permission_classes = [IsAdminUser]
    @swagger_auto_schema(
        operation_summary="Toggle User Status",
        manual_parameters=[
            openapi.Parameter(
                "pk",
                openapi.IN_PATH,
                description="User ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={200: "Status updated", 404: "User not found"}
    )
    def patch(self, request, pk):
        try:
            user = UserModel.objects.get(pk=pk)

            user.status = "blocked" if user.status != "blocked" else "user"
            user.save()

            return Response({"message": "User status updated"})

        except UserModel.DoesNotExist:
            return Response({"error": "User not found"}, status=404)



class AdminProductListCreateView(ListCreateAPIView):
    queryset = Products.objects.all().order_by("-id")
    serializer_class = AdminProductSerializer
    permission_classes = [IsAdminUser]


class AdminProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = AdminProductSerializer
    permission_classes = [IsAdminUser]




class AdminOrderListView(ListAPIView):
    queryset = Order.objects.all().prefetch_related("items", "items__product").order_by("-id")
    serializer_class = AdminOrderSerializer
    permission_classes = [IsAdminUser]


class UpdateOrderStatusView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Update Order Status",
        request_body=UpdateOrderStatusSerializer,
        manual_parameters=[
            openapi.Parameter(
                "pk",
                openapi.IN_PATH,
                description="Order ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={200: "Updated", 400: "Invalid status", 404: "Not found"}
    )
    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)

            serializer = UpdateOrderStatusSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)

            order.status = serializer.validated_data["status"]
            order.save()

            return Response({"message": "Order status updated"})

        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)



class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            total_users = UserModel.objects.count()
            total_products = Products.objects.count()
            total_orders = Order.objects.count()

            return Response({
                "users": total_users,
                "products": total_products,
                "orders": total_orders
            })

        except Exception:
            return Response({"error": "Dashboard failed"}, status=500)


class DeleteUserView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Delete User",
        manual_parameters=[
            openapi.Parameter(
                "pk",
                openapi.IN_PATH,
                description="User ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={200: "Deleted", 400: "Cannot delete admin", 404: "Not found"}
    )
    def delete(self, request, pk):
        try:
            user = UserModel.objects.get(pk=pk)

            if user.role == "admin":
                return Response(
                    {"error": "Cannot delete admin user"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.delete()
            return Response({"message": "User deleted successfully"})

        except UserModel.DoesNotExist:
            return Response({"error": "User not found"}, status=404)