from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from box_selection.models import (
    Box,
    Order,
    OrderItem,
    Product,
)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "length",
            "width",
            "height",
            "weight",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        for field in [
            "length",
            "width",
            "height",
            "weight",
        ]:
            value = attrs.get(field)

            if value is not None and value <= Decimal("0"):
                raise serializers.ValidationError(
                    {field: "Must be greater than zero."}
                )

        return attrs

    def validate(self, attrs):
        for field in [
            "length",
            "width",
            "height",
            "weight",
        ]:
            value = attrs.get(field)

            if value is not None and value <= Decimal("0"):
                raise serializers.ValidationError(
                    {field: "Must be greater than zero."}
                )

        return attrs


class BoxSerializer(serializers.ModelSerializer):
    internal_volume = serializers.DecimalField(
        max_digits=20,
        decimal_places=6,
        read_only=True,
    )

    class Meta:
        model = Box
        fields = [
            "id",
            "name",
            "internal_length",
            "internal_width",
            "internal_height",
            "max_weight",
            "cost",
            "is_active",
            "internal_volume",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "internal_volume",
            "created_at",
        ]

    def validate(self, attrs):
        positive_fields = [
            "internal_length",
            "internal_width",
            "internal_height",
            "max_weight",
        ]

        for field in positive_fields:
            value = attrs.get(field)

            if value is not None and value <= Decimal("0"):
                raise serializers.ValidationError(
                    {field: "Must be greater than zero."}
                )

        cost = attrs.get("cost")

        if cost is not None and cost < Decimal("0"):
            raise serializers.ValidationError(
                {"cost": "Cost cannot be negative."}
            )

        return attrs


class OrderItemInputSerializer(
    serializers.Serializer
):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
    )

    quantity = serializers.IntegerField(
        min_value=1
    )


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "quantity",
        ]
        read_only_fields = ["id"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemInputSerializer(
        many=True,
        write_only=True,
    )

    response_items = OrderItemSerializer(
        source="items",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "created_at",
            "items",
            "response_items",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "response_items",
        ]

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError(
                "An order must contain at least one item."
            )

        product_ids = [
            item["product"].id
            for item in items
        ]

        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError(
                "A product cannot appear more than once "
                "in the same order."
            )

        return items

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items")

        order = Order.objects.create(
            **validated_data
        )

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                )
                for item in items_data
            ]
        )

        return order