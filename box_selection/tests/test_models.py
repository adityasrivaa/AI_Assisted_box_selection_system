from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from box_selection.models import (
    Box,
    Order,
    OrderItem,
    Product,
)


class ProductModelTests(TestCase):

    def test_product_creation(self):
        product = Product.objects.create(
            name="Laptop",
            length=Decimal("30.00"),
            width=Decimal("20.00"),
            height=Decimal("2.00"),
            weight=Decimal("1.500"),
        )

        self.assertEqual(product.name, "Laptop")
        self.assertEqual(
            product.weight,
            Decimal("1.500"),
        )


class BoxModelTests(TestCase):

    def test_box_creation(self):
        box = Box.objects.create(
            name="Medium Box",
            internal_length=Decimal("40.00"),
            internal_width=Decimal("30.00"),
            internal_height=Decimal("20.00"),
            max_weight=Decimal("10.000"),
            cost=Decimal("5.00"),
        )

        self.assertEqual(
            box.cost,
            Decimal("5.00"),
        )

        self.assertEqual(
            box.internal_volume,
            Decimal("24000.00"),
        )


class OrderModelTests(TestCase):

    def test_order_creation(self):
        order = Order.objects.create()

        self.assertIsNotNone(order.id)

    def test_order_item_quantity(self):
        product = Product.objects.create(
            name="Keyboard",
            length=Decimal("30.00"),
            width=Decimal("15.00"),
            height=Decimal("5.00"),
            weight=Decimal("0.700"),
        )

        order = Order.objects.create()

        item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=3,
        )

        self.assertEqual(item.quantity, 3)

    def test_duplicate_product_in_same_order_is_not_allowed(self):
        product = Product.objects.create(
            name="Mouse",
            length=Decimal("10.00"),
            width=Decimal("5.00"),
            height=Decimal("3.00"),
            weight=Decimal("0.200"),
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
        )

        duplicate = OrderItem(
            order=order,
            product=product,
            quantity=2,
        )

        with self.assertRaises(ValidationError):
            duplicate.validate_constraints()