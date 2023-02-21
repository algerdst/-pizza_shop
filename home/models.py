from django.db import models

from users.models import User


class Category(models.Model):
    category_name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=15, default='')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Ingredient(models.Model):
    name = models.CharField(max_length=25, unique=True)

    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='')
    name = models.CharField(max_length=40)
    price = models.IntegerField(default=100)
    image = models.ImageField(upload_to='media/images', default='default_pizza.jpg')
    consist = models.ManyToManyField(Ingredient, blank=True)
    slug = models.SlugField(default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user}| Товар {self.product}'

    def summa(self):
        return self.product.price * self.quantity
