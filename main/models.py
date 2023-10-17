from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.FloatField(default=1)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def create(self, validated_data):
        return super().save(**validated_data)


class Meta:
    verbose_name = _('Product')
    verbose_name_plural = _('Products')


class Picture(models.Model):
    image = models.ImageField(upload_to='pics')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Picture')
        verbose_name_plural = _('Pictures')


class ShoppingCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], default=1
    )
    uploaded_date = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='pics')
    price = models.FloatField()
    uploaded_date = models.DateTimeField(auto_now_add=True)
