from django.db import models

# Create your models here.
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

class Product(models.Model):
    name = models.CharField(max_length=200)
    
    length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    width = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.001"))],
    )

    craeted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name

    def clean(self):
        dimensions = {
            "length": self.length,
            "width": self.width,
            "height": self.height,
            "weight": self.weight,
        }

        for field_name, value in dimensions.items():
            if value is not None and value <= 0:
                raise ValidationError(
                    {field_name: "Value must be greater than zero."}
                )

class Box(models.Model):
    name = models.CharField(max_length=200)

    internal_length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    internal_width = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    internal_height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    max_weight = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        validators=[MinValueValidator(Decimal("0.001"))],
    )

    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["cost", "id"]

    def __str__(self):
        return self.name

    @property
    def internal_volume(self):
        return(
            self.internal_length
            * self.internal_width
            * self.internal_height
        )

    def clean(self):
        dimensions = {
            "internal_length": self.internal_length,
            "internal_width": self.internal_width,
            "internal_height": self.internal_height,
            "max_weight": self.max_weight,
            "cost": self.cost,
        }


        for field_name, value in dimensions.items():
            if value is not None and value < 0:
                raise ValidationError(
                    {field_name: "Value cannot be negative."}
                )

        if (
            self.internal_length is not None
            and self.internal_length <= 0
        ):
            raise ValidationError(
                {"internal_length": "Length must be greater than zero."}
            )

        if (
            self.internal_width is not None
            and self.internal_width <= 0
        ):
            raise ValidationError(
                {"internal_width": "Width must be greater than zero."}
            )

        if (
            self.internal_height is not None
            and self.internal_height <= 0
        ):
            raise ValidationError(
                {"internal_height": "Height must be greater than zero."}
            )

        if self.max_weight is not None and self.max_weight <= 0:
            raise ValidationError(
                {"max_weight": "Maximum weight must be greater than zero."}
            )

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items",
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["order", "product"],
                name="unique_product_per_order",
            )
        ]

    def __str__(self):
        return (
            f"{self.product.name} x {self.quantity}"
        )

    def clean(self):
        if self.quantity < 1:
            raise ValidationError(
                {"quantity": "Quantity must be at least 1."}
            )