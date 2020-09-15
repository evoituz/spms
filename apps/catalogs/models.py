from django.db import models

from apps.main.models import *


class Algorithm(models.Model):
    name = models.CharField('Алгоритм', max_length=250, blank=True)

    class Meta:
        verbose_name = 'Алгоритм'
        verbose_name_plural = 'Алгоритмы'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Название товара', max_length=250, blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class ProductProfile(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', related_name='profiles', on_delete=models.CASCADE,
                                null=True)

    name = models.CharField('Название профиля', max_length=250, blank=True)

    algorithm = models.ForeignKey(Algorithm, verbose_name='Алгоритм', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.name


class ProductProfileSize(models.Model):
    product_profile = models.ForeignKey(ProductProfile, verbose_name='Профиль товара', related_name='sizes',
                                        on_delete=models.CASCADE, null=True)
    size = models.CharField('Размер', max_length=250, blank=True)

    price_usd = models.DecimalField('Цена в USD', decimal_places=2, max_digits=12, null=True, blank=True)
    price_uzs = models.DecimalField('Цена в UZS', decimal_places=0, max_digits=15, null=True, blank=True)

    sell_price_usd = models.DecimalField('Цена продажи в USD', decimal_places=2, max_digits=12, null=True, blank=True)
    sell_price_uzs = models.DecimalField('Цена продажи в UZS', decimal_places=0, max_digits=15, null=True, blank=True)
    notes = models.TextField('Заметки', blank=True)

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def save(self, *args, **kwargs):
        if not self.price_uzs and self.price_usd:
            conf = GeneralSettings().load()
            self.price_uzs = self.price_usd * conf.course_usd_to_uzs
        super().save(*args, **kwargs)

    def get_algorithm(self):
        alg = self.product_profile.algorithm.id
        items = self.items.all()
        a = items[0].value
        b = items[1].value
        c = items[2].value
        if alg == 1:
            return round(b + (c / a), 3)
        if alg == 2:
            return round((b + c) / a, 3)
        if alg == 3:
            d = items[3].value
            return round((c + d) / (1000 / a) * 2, 3)
        if alg == 4:
            d = items[3].value
            return round((c + d) / (1000 / a), 3)

    def get_uzs(self):
        conf = GeneralSettings().load()
        return round(self.get_algorithm() * float(conf.course_usd_to_uzs))

    def __str__(self):
        return self.size


class ProductProfileSizeItem(models.Model):
    size = models.ForeignKey(ProductProfileSize, verbose_name='Размер', related_name='items', on_delete=models.CASCADE,
                             null=True)
    name = models.CharField('Имя атрибута', max_length=250, blank=True)
    value = models.FloatField('Значение атрибута', null=True, blank=True)

    class Meta:
        verbose_name = 'Атрибут'
        verbose_name_plural = 'Атрибуты'
        ordering = ['id']

    def __str__(self):
        return self.name
