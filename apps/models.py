from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    class Status(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        CLIENT = 'client', 'Client'
        VIP_CLIENT = 'vip_client', 'Vip client'

    status = models.CharField(max_length=50, choices=Status.choices, default=Status.CLIENT)
    email = models.EmailField(unique=True)



class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(BaseModel):
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    short_description = models.TextField()
    description = models.TextField(blank=True, null=True)
    discount = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField()
    is_premium = models.BooleanField(default=False)
    shopping_cost = models.SmallIntegerField(default=0)
    tags = models.ForeignKey('apps.Tag', models.CASCADE, blank=True, default=1)
    specification = models.JSONField(default=dict, blank=True)
    author = models.ForeignKey('apps.User', models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def discount_price(self):
        return self.price - self.price * self.discount // 100


class ProductImage(models.Model):
    product = models.ForeignKey('apps.Product', models.CASCADE, 'images')
    image = models.ImageField(upload_to='product/images/')


class Wishlist(models.Model):
    product = models.ForeignKey('apps.Product', models.CASCADE)
    user = models.ForeignKey('apps.User', models.CASCADE)


class Cart(BaseModel):
    user = models.ForeignKey('apps.User', models.CASCADE)
    is_active = models.BooleanField(default=False)


class CartItem(BaseModel):
    product = models.ForeignKey('apps.Product', models.CASCADE)
    cart = models.ForeignKey('apps.Cart', models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()

# class Order(BaseModel):
#     class Status(models.TextChoices):
#         CREATED = 'created', 'yaratilgan'
#         WAITING = 'waiting', 'tolanayotgan'
#         PAID = 'paid', 'tolangan'
#         CANCELLED = 'cancelled', 'bekor qilingan'
#
#     cart = models.OneToOneField('apps.Cart', models.CASCADE)
#     user = models.ForeignKey('apps.User', models.CASCADE)
#     status = models.CharField(max_length=25, choices=Status.choices, default=Status.CREATED)
