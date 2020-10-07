from django.db import models


class StockCategory(models.Model):
    name = models.CharField('Название товара', max_length=250, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['id']

    def __str__(self):
        return self.name


class Stock(models.Model):
    PIECES = 'pc'
    GRAM = 'g'
    METER = 'm'

    PRODUCT_TYPE = (
        (PIECES, 'шт.'),
        (GRAM, 'гр.'),
        (METER, 'метр'),
    )

    category = models.ForeignKey(StockCategory, verbose_name='Товар', on_delete=models.CASCADE)
    profile_name = models.CharField('Профиль', max_length=250, blank=True)
    size = models.CharField('Размер', max_length=250)
    quantity = models.IntegerField('Количество штук/вес/метров')
    type_product = models.CharField('Тип товара', max_length=50, choices=PRODUCT_TYPE)
    # Цена указываются лишь за 1шт/1000гр/1м
    price_purchase = models.DecimalField('Цена покупки/Стоимость', max_digits=12, decimal_places=0, default=0)
    price_arrival = models.DecimalField('Приходная цена/Обошлась', max_digits=12, decimal_places=0, default=0)
    price_sell = models.DecimalField('Цена продажи', max_digits=12, decimal_places=0)

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склад"
        ordering = ['id']

    def __str__(self):
        return self.size
