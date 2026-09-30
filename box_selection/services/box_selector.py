from dataclasses import dataclass
from decimal import Decimal
from itertools import permutations
from typing import Iterable

from django.db.models import QuerySet

from box_selection.models import Box, Order, OrderItem, Product


@dataclass(frozen=True)
class Dimensions:
    length: Decimal
    width: Decimal
    height: Decimal

    @property
    def volume(self) -> Decimal:
        return (
            self.length
            * self.width
            * self.height
        )


@dataclass(frozen=True)
class FreeSpace:
    length: Decimal
    width: Decimal
    height: Decimal


@dataclass(frozen=True)
class PackingItem:
    product: Product
    quantity_index: int

    @property
    def dimensions(self) -> Dimensions:
        return Dimensions(
            length=self.product.length,
            width=self.product.width,
            height=self.product.height,
        )


@dataclass(frozen=True)
class BoxSelectionResult:
    box: Box | None
    total_weight: Decimal
    reason: str


class BoxSelector:
    """
    Selects the cheapest active box capable of containing an order.

    Packing strategy:
    - Products are expanded according to quantity.
    - Larger products are packed first.
    - All unique product rotations are considered.
    - A simple free-space splitting heuristic is used.
    - The algorithm does not guarantee globally optimal 3D packing.
    """

    def select_box(self, order: Order) -> BoxSelectionResult:
        order_items = list(
            order.items.select_related("product").all()
        )

        if not order_items:
            return BoxSelectionResult(
                box=None,
                total_weight=Decimal("0"),
                reason="The order contains no items.",
            )

        total_weight = self.calculate_total_weight(
            order_items
        )

        boxes = Box.objects.filter(
            is_active=True,
            max_weight__gte=total_weight,
        ).order_by(
            "cost",
            "internal_length",
            "internal_width",
            "internal_height",
            "id",
        )

        for box in boxes:
            if self.can_pack_order(order_items, box):
                return BoxSelectionResult(
                    box=box,
                    total_weight=total_weight,
                    reason=(
                        "Selected as the cheapest active box "
                        "that satisfies weight and packing "
                        "constraints."
                    ),
                )

        return BoxSelectionResult(
            box=None,
            total_weight=total_weight,
            reason=(
                "No active box can accommodate the order "
                "using the configured packing heuristic."
            ),
        )

    @staticmethod
    def calculate_total_weight(
        order_items: Iterable[OrderItem],
    ) -> Decimal:
        total_weight = Decimal("0")

        for item in order_items:
            total_weight += (
                item.product.weight
                * item.quantity
            )

        return total_weight

    def can_pack_order(
        self,
        order_items: list[OrderItem],
        box: Box,
    ) -> bool:
        total_weight = self.calculate_total_weight(
            order_items
        )

        if total_weight > box.max_weight:
            return False

        packing_items = self.expand_order_items(
            order_items
        )

        packing_items.sort(
            key=lambda item: item.dimensions.volume,
            reverse=True,
        )

        free_spaces = [
            FreeSpace(
                length=box.internal_length,
                width=box.internal_width,
                height=box.internal_height,
            )
        ]

        for item in packing_items:
            placed = self._place_item(
                item.dimensions,
                free_spaces,
            )

            if placed is None:
                return False

            free_spaces = placed

        return True

    @staticmethod
    def expand_order_items(
        order_items: Iterable[OrderItem],
    ) -> list[PackingItem]:
        expanded_items = []

        for order_item in order_items:
            for quantity_index in range(
                order_item.quantity
            ):
                expanded_items.append(
                    PackingItem(
                        product=order_item.product,
                        quantity_index=quantity_index,
                    )
                )

        return expanded_items

    def _place_item(
        self,
        dimensions: Dimensions,
        free_spaces: list[FreeSpace],
    ) -> list[FreeSpace] | None:
        orientations = self._get_orientations(
            dimensions
        )

        for space_index, space in enumerate(
            free_spaces
        ):
            for orientation in orientations:
                if self._fits(
                    orientation,
                    space,
                ):
                    remaining_spaces = (
                        free_spaces[:space_index]
                        + free_spaces[space_index + 1:]
                    )

                    remaining_spaces.extend(
                        self._split_space(
                            space,
                            orientation,
                        )
                    )

                    remaining_spaces = (
                        self._remove_redundant_spaces(
                            remaining_spaces
                        )
                    )

                    return remaining_spaces

        return None

    @staticmethod
    def _get_orientations(
        dimensions: Dimensions,
    ) -> list[Dimensions]:
        values = (
            dimensions.length,
            dimensions.width,
            dimensions.height,
        )

        unique_orientations = set(
            permutations(values)
        )

        return [
            Dimensions(
                length=orientation[0],
                width=orientation[1],
                height=orientation[2],
            )
            for orientation in unique_orientations
        ]

    @staticmethod
    def _fits(
        item: Dimensions,
        space: FreeSpace,
    ) -> bool:
        return (
            item.length <= space.length
            and item.width <= space.width
            and item.height <= space.height
        )

    @staticmethod
    def _split_space(
        space: FreeSpace,
        item: Dimensions,
    ) -> list[FreeSpace]:
        """
        Split a free rectangular space after placing an item
        at its lower-left-front corner.

        The resulting regions are:
        1. Space to the right of the item.
        2. Space behind the item.
        3. Space above the item.

        These regions form a simple non-overlapping partition
        of the remaining rectangular space.
        """

        remaining_spaces = []

        right_length = (
            space.length - item.length
        )

        if right_length > 0:
            remaining_spaces.append(
                FreeSpace(
                    length=right_length,
                    width=space.width,
                    height=space.height,
                )
            )

        behind_width = (
            space.width - item.width
        )

        if behind_width > 0:
            remaining_spaces.append(
                FreeSpace(
                    length=item.length,
                    width=behind_width,
                    height=space.height,
                )
            )

        above_height = (
            space.height - item.height
        )

        if above_height > 0:
            remaining_spaces.append(
                FreeSpace(
                    length=item.length,
                    width=item.width,
                    height=above_height,
                )
            )

        return remaining_spaces

    @staticmethod
    def _remove_redundant_spaces(
        spaces: list[FreeSpace],
    ) -> list[FreeSpace]:
        """
        Remove duplicate or zero-sized free spaces.

        A more advanced implementation could also remove
        geometrically contained spaces, but that is unnecessary
        for this assignment.
        """

        unique_spaces = []

        seen = set()

        for space in spaces:
            dimensions = (
                space.length,
                space.width,
                space.height,
            )

            if any(value <= 0 for value in dimensions):
                continue

            if dimensions in seen:
                continue

            seen.add(dimensions)
            unique_spaces.append(space)

        return unique_spaces