from django.conf import settings
from django.core.mail import send_mail
from django.db import models

from users.models import User


class Order(models.Model):
    CREATED = 0
    IN_WORK = 1
    SUCCESS = 2
    CANCELED = 3
    STATUSES = (
        (CREATED, "Создан"),
        (IN_WORK, "В работе"),
        (SUCCESS, "Доставлен/Оплачен"),
        (CANCELED, "Отменен"),
    )
    BY_CASH = 0
    BY_CARD = 1
    PAYMENT_METHOD = (
        (BY_CASH, 'Наличными'),
        (BY_CARD, 'Картой'),
    )
    first_name = models.CharField(max_length=64)
    number = models.CharField(default='', max_length=20)  # Номер телефона клиента
    address = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    comment = models.TextField(default='', blank=True)
    payment = models.SmallIntegerField(default=BY_CASH, choices=PAYMENT_METHOD)
    content = models.TextField(max_length=1000, default='')
    waiting_time = models.SmallIntegerField(default=0)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Заказ #{self.id} для {self.first_name} от пользователя {self.initiator}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def send_order(self):
        send_mail(
            '',
            f'''Заказ для {self.first_name}\nСодержание заказа: {self.content}\nЗаберет через {self.waiting_time} минут
            \nНомер телефона: {self.number}\nКомментарий к заказу: {self.comment}\nАдрес доставки: {self.address}\n
            Способ оплаты: {self.payment}
            ''',
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER]
        )
