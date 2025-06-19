import os
import random
import qrcode
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

from .managers import CustomUserManager
from .choices import *


class User(AbstractUser):
    username = models.CharField("Имя пользователя", max_length=255)
    phone = models.CharField("Номер телефона", unique=True)

    code = models.IntegerField("Код активации", null=True, blank=True)
    activated = models.BooleanField("Активировано", default=False)

    bonus_id = models.CharField("Бонусный ID", null=True, blank=True)
    bonus = models.DecimalField("Бонус пользователя", max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    qrimg = models.ImageField("QRcode Пользователя", null=True, blank=True)

    notification = models.BooleanField("Получать уведомления", default=False)

    USERNAME_FIELD = "phone"
    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        bonus_id = f"{1000200030004000 + int(self.id)}"
        self.bonus_id = bonus_id

        self.code = int(random.randint(100_000, 999_999))

        qr = qrcode.make(str(bonus_id), border=2)
        qr_path = f"user/bonus-qr/{bonus_id}.png"
        qr.save(os.path.join(settings.MEDIA_ROOT, qr_path))
        self.qrimg.name = qr_path

        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"