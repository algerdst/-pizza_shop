from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    image = models.ImageField(upload_to='profile_pics', default='default_profile.jpg')
    is_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=15, unique=True)
    orders_history = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = 'Пользователь сайта'
        verbose_name_plural = 'Пользователи сайта'


class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.UUIDField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'Верификация для {self.user.email}'

    def send_verification_email(self):
        link = reverse('verify', kwargs={'email': self.user.email, 'code': self.code})
        verify_link = f'{settings.DOMAIN_NAME}{link}'
        send_mail(
            f'Верификация аккаунта для {self.user.email}',
            f'Для подтверждения аккаунта перейдите по ссылке {verify_link}',
            settings.EMAIL_HOST_USER,
            [self.user.email],
        )
