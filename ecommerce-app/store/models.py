from django.db import models
from django.contrib.auth.models import User


# ===========================
# Category
# ===========================

class Category(models.Model):

    name = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

    @property
    def image_key(self):
        image_keys = {
            "electronics": "electronics",
            "fashion": "fashion",
            "books": "books",
            "accessories": "accessories",
            "home & kitchen": "home-kitchen",
        }
        return f"images/categories/{image_keys.get(self.name.lower(), 'default')}.svg"


# ===========================
# Product
# ===========================

class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

# ===========================
# Order
# ===========================

class Order(models.Model):

    STATUS_CHOICES = [

        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),

    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(
        max_length=200
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=15
    )

    address = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def total(self):

        total_price = 0

        for item in self.items.all():

            total_price += (
                item.product.price *
                item.quantity
            )

        return total_price

    def __str__(self):

        return f"Order #{self.id}"


# ===========================
# Order Item
# ===========================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def subtotal(self):

        return self.product.price * self.quantity

    def __str__(self):

        return self.product.name


class OrderRequest(models.Model):

    REQUEST_TYPES = [
        ("Return", "Return"),
        ("Exchange", "Exchange"),
    ]

    STATUS_CHOICES = [
        ("Requested", "Requested"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Completed", "Completed"),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_requests")
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="requests")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_requests")
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPES)
    reason = models.CharField(max_length=200)
    details = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="Requested")
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.request_type} request for Order #{self.order_id}"