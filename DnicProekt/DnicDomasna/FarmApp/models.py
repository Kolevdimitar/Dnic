from PIL import Image

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/',blank=True,null=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            max_size = (300, 300)
            img.thumbnail(max_size)
            img.save(self.image.path)


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    products = models.ManyToManyField(Product,through='CartItem')

    def __str__(self) -> str:
        return f"{self.user}'s cart"

    def total_quantity(self):
        return sum(cart_item.quantity for cart_item in self.cartitem_set.all())

    def total_cost(self):
        return sum(cart_item.product.price * cart_item.quantity for cart_item in self.cartitem_set.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart}"

class Order(models.Model):
    products = models.ManyToManyField(Product,through='OrderItem')
    order_date = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=15)

    def __str__(self):
        return f"Order {self.order_id}"

    def total_amount(self):
        return sum(order_item.product.price * order_item.quantity for order_item in self.orderitem_set.all())

    def get_cart_items(self):
        cart_items = []
        for order_item in self.orderitem_set.all():
            product = order_item.product
            quantity = order_item.quantity
            cart_items.append((product, quantity))
        return cart_items

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    order_quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.order}"
