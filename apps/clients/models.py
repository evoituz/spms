from django.db import models


class Client(models.Model):
    name = models.CharField('Имя клиента', max_length=250)
    balance = models.DecimalField('Баланс', max_digits=25, decimal_places=0,
                                  default=0)  # При транзакции, необходимо записывать оплату сюда. Если долг минусовать, если оплатили плюсовать

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['id', ]

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(Client, verbose_name='Клиент', on_delete=models.CASCADE, blank=True, null=True)

    created_dt = models.DateTimeField('Дата и время покупки', auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def get_total_price(self):
        return sum([item.price for item in self.items.all()])

    def get_items_to_string(self):
        items = list(self.items.values('product_title', 'quantity', 'price'))
        result = [f'{i+1}) {item["product_title"]}: {item["quantity"]} - {item["price"]} сум' for i, item in enumerate(items)]
        print(result)
        return result

    def get_transaction(self):
        obj = Transaction.objects.get(order_id=self.id)
        return {'amount': obj.amount, 'paid': True if obj.paid == 'payment' else False}

    def get_pay(self):
        transaction = self.get_transaction()
        print(transaction['paid'])
        if transaction['paid']:
            return transaction['amount']
        return 0

    def get_debt(self):
        transaction = self.get_transaction()
        if not transaction['paid']:
            return transaction['amount']
        return 0



    def __str__(self):
        return 'Order #%s' % self.id


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='items', on_delete=models.CASCADE)
    product_title = models.CharField('Название товара',
                                     max_length=250)  # StockCategory.name Stock.profile_nam Stock.size
    quantity = models.CharField('Количество',
                                max_length=250)  # Количество и тип количество (4000 гр.) 300гр./3шт./230м.
    price = models.DecimalField('Общая сумма', max_digits=15, decimal_places=0)

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказа'

    def __str__(self):
        return self.product_title


class Transaction(models.Model):
    DEBT = 'debt'
    PAYMENT = 'payment'
    PAID_STATUS = (
        (DEBT, 'В долг'),
        (PAYMENT, 'Оплачено'),
    )

    client = models.ForeignKey(Client, verbose_name='Клиент', on_delete=models.CASCADE, blank=True,
                               null=True)  # Не всегда может быть указан клиент, так как покупатель может быть проходцем.
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE,
                              blank=True,
                              null=True)  # Не всегда оплата может производится за заказ, к примеру внесли часть долга
    amount = models.DecimalField('Сумма', max_digits=15, decimal_places=0)
    paid = models.CharField('Оплата', choices=PAID_STATUS, max_length=50)  # На случай, если заказ был совершён в долг

    created_dt = models.DateTimeField('Дата и время покупки', auto_now_add=True)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        try:
            value = str(self.order.created_dt)
        except AttributeError:
            value = self.client.name

        return value
