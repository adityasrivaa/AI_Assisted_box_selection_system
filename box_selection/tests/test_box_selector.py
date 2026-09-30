from decimal import Decimal

from django.test import TestCase

from box_selection.models import (
    Box,
    Order,
    OrderItem,
    Product,
)
from box_selection.services.box_selector import (
    BoxSelector,
    Dimensions,
)


class BoxSelectorTests(TestCase):

    def setUp(self):
        self.selector = BoxSelector()

    def create_product(
        self,
        name="Product",
        length="10.00",
        width="5.00",
        height="2.00",
        weight="1.000",
    ):
        return Product.objects.create(
            name=name,
            length=Decimal(length),
            width=Decimal(width),
            height=Decimal(height),
            weight=Decimal(weight),
        )

    def create_box(
        self,
        name="Box",
        length="20.00",
        width="20.00",
        height="20.00",
        max_weight="100.000",
        cost="10.00",
        is_active=True,
    ):
        return Box.objects.create(
            name=name,
            internal_length=Decimal(length),
            internal_width=Decimal(width),
            internal_height=Decimal(height),
            max_weight=Decimal(max_weight),
            cost=Decimal(cost),
            is_active=is_active,
        )

    def test_product_fits_without_rotation(self):
        product = Dimensions(
            Decimal("10"),
            Decimal("5"),
            Decimal("2"),
        )

        box = Dimensions(
            Decimal("20"),
            Decimal("10"),
            Decimal("5"),
        )

        self.assertTrue(
            self.selector._fits(
                product,
                box,
            )
        )

    def test_product_fits_with_rotation(self):
        product = Dimensions(
            Decimal("10"),
            Decimal("20"),
            Decimal("5"),
        )

        box = Dimensions(
            Decimal("5"),
            Decimal("10"),
            Decimal("20"),
        )

        orientations = (
            self.selector._get_orientations(
                product
            )
        )

        fits = any(
            self.selector._fits(
                orientation,
                box,
            )
            for orientation in orientations
        )

        self.assertTrue(fits)

    def test_product_too_large_for_box(self):
        product = self.create_product(
            length="100",
            width="100",
            height="100",
        )

        box = self.create_box(
            length="20",
            width="20",
            height="20",
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
        )

        self.assertFalse(
            self.selector.can_pack_order(
                list(order.items.all()),
                box,
            )
        )

    def test_order_exceeding_weight_capacity(self):
        product = self.create_product(
            weight="10.000"
        )

        box = self.create_box(
            max_weight="5.000"
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
        )

        self.assertFalse(
            self.selector.can_pack_order(
                list(order.items.all()),
                box,
            )
        )

    def test_multiple_products(self):
        product_a = self.create_product(
            name="A",
            length="5",
            width="5",
            height="5",
            weight="1",
        )

        product_b = self.create_product(
            name="B",
            length="5",
            width="5",
            height="5",
            weight="1",
        )

        box = self.create_box(
            length="10",
            width="5",
            height="5",
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product_a,
            quantity=1,
        )

        OrderItem.objects.create(
            order=order,
            product=product_b,
            quantity=1,
        )

        self.assertTrue(
            self.selector.can_pack_order(
                list(order.items.all()),
                box,
            )
        )

    def test_multiple_quantities(self):
        product = self.create_product(
            length="5",
            width="5",
            height="5",
            weight="1",
        )

        box = self.create_box(
            length="10",
            width="5",
            height="5",
            max_weight="10",
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=2,
        )

        order_items = list(
            order.items.all()
        )

        self.assertEqual(
            self.selector.calculate_total_weight(
                order_items
            ),
            Decimal("2.000"),
        )

        self.assertTrue(
            self.selector.can_pack_order(
                order_items,
                box,
            )
        )

    def test_cheapest_suitable_box_is_selected(self):
        product = self.create_product(
            length="5",
            width="5",
            height="5",
        )

        expensive_box = self.create_box(
            name="Expensive",
            length="10",
            width="10",
            height="10",
            cost="20",
        )

        cheap_box = self.create_box(
            name="Cheap",
            length="10",
            width="10",
            height="10",
            cost="5",
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
        )

        result = self.selector.select_box(order)

        self.assertIsNotNone(result.box)
        self.assertEqual(
            result.box.id,
            cheap_box.id,
        )

    def test_no_suitable_box_available(self):
        product = self.create_product(
            length="100",
            width="100",
            height="100",
        )

        self.create_box(
            name="Small",
            length="10",
            width="10",
            height="10",
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
        )

        result = self.selector.select_box(order)

        self.assertIsNone(result.box)

    def test_inactive_box_is_not_selected(self):
        product = self.create_product(
            length="5",
            width="5",
            height="5",
        )

        self.create_box(
            name="Inactive",
            length="10",
            width="10",
            height="10",
            cost="1",
            is_active=False,
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
        )

        result = self.selector.select_box(order)

        self.assertIsNone(result.box)

    def test_empty_order_has_no_recommendation(self):
        order = Order.objects.create()

        result = self.selector.select_box(order)

        self.assertIsNone(result.box)

        self.assertEqual(
            result.total_weight,
            Decimal("0"),
        )