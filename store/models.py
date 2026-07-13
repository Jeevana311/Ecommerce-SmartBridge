from django.db import models
from django.contrib.auth.models import User


# ===========================
# Category
# ===========================

class Category(models.Model):

    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name



# ===========================
# Product
# ===========================

class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    name = models.CharField(
        max_length=200
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to='products/'
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return self.name



# ===========================
# Order
# ===========================

class Order(models.Model):

    STATUS_CHOICES = [

        ('Pending','Pending'),
        ('Processing','Processing'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),

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
        default='Pending'
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

        related_name='items'

    )


    product = models.ForeignKey(

        Product,

        on_delete=models.CASCADE

    )


    quantity = models.PositiveIntegerField(

        default=1

    )


    def __str__(self):

        return self.product.name