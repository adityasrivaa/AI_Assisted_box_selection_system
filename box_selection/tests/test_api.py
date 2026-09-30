from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase

from box_selection.models import (
    Box,
    Order,
    Product,
)


class BoxSelectionAPITests(APITestCase):

    def create_product(self):
        return Product.objects.create(
            name="Laptop",
            length=Decimal("30"),
            width=Decimal("20"),
            height=Decimal("2"),
            weight=Decimal("1.500"),
        )

    def create_box(
        self,
        name="Box",
        cost="10.00",
        length="40",
        width="30",
        height="20",
        max_weight="10",
    ):
        return Box.objects.create(
            name=name,
            internal_length=Decimal(length),
            internal_width=Decimal(width),
            internal_height=Decimal(height),
            max_weight=Decimal(max_weight),
            cost=Decimal(cost),
        )

    def test_product_creation_api(self):
        response = self.client.post(
            "/api/products/",
            {
                "name": "Laptop",
                "length": "30.00",
                "width": "20.00",
                "height": "2.00",
                "weight": "1.500",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["name"],
            "Laptop",
        )

    def test_box_creation_api(self):
        response = self.client.post(
            "/api/boxes/",
            {
                "name": "Medium Box",
                "internal_length": "40.00",
                "internal_width": "30.00",
                "internal_height": "20.00",
                "max_weight": "10.000",
                "cost": "5.00",
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_order_creation_api(self):
        product = self.create_product()

        response = self.client.post(
            "/api/orders/",
            {
                "items": [
                    {
                        "product_id": product.id,
                        "quantity": 2,
                    }
                ]
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        order_id = response.data["id"]

        order = Order.objects.get(
            id=order_id
        )

        self.assertEqual(
            order.items.count(),
            1,
        )

        self.assertEqual(
            order.items.first().quantity,
            2,
        )

    def test_empty_order_is_rejected(self):
        response = self.client.post(
            "/api/orders/",
            {
                "items": []
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_recommended_box_endpoint(self):
        product = self.create_product()

        self.create_box(
            name="Box A",
            cost="10",
        )

        order_response = self.client.post(
            "/api/orders/",
            {
                "items": [
                    {
                        "product_id": product.id,
                        "quantity": 1,
                    }
                ]
            },
            format="json",
        )

        self.assertEqual(
            order_response.status_code,
            status.HTTP_201_CREATED,
        )

        order_id = order_response.data["id"]

        response = self.client.get(
            f"/api/orders/{order_id}/recommended-box/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["order_id"],
            order_id,
        )

        self.assertEqual(
            response.data["selected_box"]["name"],
            "Box A",
        )

        self.assertEqual(
            response.data["total_order_weight"],
            "1.500",
        )

    def test_recommendation_when_no_box_exists(self):
        product = self.create_product()

        self.create_box(
            name="Tiny Box",
            cost="2",
            length="5",
            width="5",
            height="5",
            max_weight="1",
        )

        order_response = self.client.post(
            "/api/orders/",
            {
                "items": [
                    {
                        "product_id": product.id,
                        "quantity": 1,
                    }
                ]
            },
            format="json",
        )

        order_id = order_response.data["id"]

        response = self.client.get(
            f"/api/orders/{order_id}/recommended-box/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

        self.assertIsNone(
            response.data["selected_box"]
        )

    def test_invalid_product_dimensions_are_rejected(self):
        response = self.client.post(
            "/api/products/",
            {
                "name": "Invalid Product",
                "length": "0",
                "width": "20",
                "height": "2",
                "weight": "1",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )