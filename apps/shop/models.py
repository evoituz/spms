from django.db import models


class ProductCategory(models.Model):
    """Имя товара"""
    name = models.CharField('Категория', max_length=250)

    class Meta:
        verbose_name = "Категория товаров"
        verbose_name_plural = "Категории товаров"

    def __str__(self):
        return self.name


class Product(models.Model):
    PIECES = 'pc'
    GRAM = 'g'
    METER = 'm'

    QUANTITY_TYPE = (
        (PIECES, 'шт.'),
        (GRAM, 'гр.'),
        (METER, 'метр'),
    )

    category = models.ForeignKey(ProductCategory, verbose_name='Категория', on_delete=models.CASCADE)
    profile = models.CharField('Профиль', max_length=250, blank=True)
    size = models.CharField('Размер', max_length=250)
    quantity = models.IntegerField('Количество', default=0)
    type_quantity = models.CharField('Тип количество', max_length=250, choices=QUANTITY_TYPE, default=PIECES)
    price_uzs = models.DecimalField('Цена в суммах', max_digits=12, decimal_places=0)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['id']

    def __str__(self):
        return self.size
