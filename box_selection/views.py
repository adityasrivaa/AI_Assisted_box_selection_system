from django.shortcuts import render

# Create your views here.
from django.db.models import Prefetch
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from box_selection.models import Box, Order, OrderItem, Product
from box_selection.serializers import (
    BoxSerializer,
    OrderSerializer,
    ProductSerializer,
)
from box_selection.services.box_selector import (
    BoxSelector,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class BoxViewSet(viewsets.ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related(
        Prefetch(
            "items",
            queryset=OrderItem.objects.select_related(
                "product"
            ),
        )
    ).all()

    serializer_class = OrderSerializer


class RecommendedBoxView(APIView):
    """
    Return the cheapest active box capable of
    accommodating the specified order.
    """

    def get(self, request, order_id):
        try:
            order = (
                Order.objects
                .prefetch_related(
                    Prefetch(
                        "items",
                        queryset=OrderItem.objects.select_related(
                            "product"
                        ),
                    )
                )
                .get(pk=order_id)
            )
        except Order.DoesNotExist:
            return Response(
                {
                    "detail": "Order not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        selector = BoxSelector()

        result = selector.select_box(order)

        if result.box is None:
            return Response(
                {
                    "order_id": order.id,
                    "selected_box": None,
                    "total_order_weight": str(
                        result.total_weight
                    ),
                    "reason": result.reason,
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        box = result.box

        return Response(
            {
                "order_id": order.id,
                "selected_box": {
                    "id": box.id,
                    "name": box.name,
                    "dimensions": {
                        "length": str(
                            box.internal_length
                        ),
                        "width": str(
                            box.internal_width
                        ),
                        "height": str(
                            box.internal_height
                        ),
                    },
                    "max_weight": str(
                        box.max_weight
                    ),
                    "cost": str(box.cost),
                },
                "total_order_weight": str(
                    result.total_weight
                ),
                "reason": result.reason,
            },
            status=status.HTTP_200_OK,
        )