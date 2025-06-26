import os
import random
import qrcode
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from .managers import CustomUserManager

class BonusId(models.Model):
    bonus_id = models.CharField(max_length=8, unique=True, primary_key=True)

    def __str__(self):
        return self.bonus_id

    @staticmethod
    def generate_bonus_id():
        last_bonus = BonusId.objects.order_by('bonus_id').last()
        if last_bonus:
            last_number = int(last_bonus.bonus_id)
            new_number = last_number + 1
        else:
            new_number = 1
        return f"{new_number:08d}"

    class Meta:
        app_label = 'users'
        verbose_name = 'Генерация бонусных карточек'
        verbose_name_plural = 'Генерация бонусных карточек'

class BonusCard(models.Model):
    user = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, verbose_name='Клиент')
    bonus_id = models.ForeignKey("BonusId", on_delete=models.CASCADE, verbose_name='Уникальный номер карты')

    def __str__(self):
        return str(self.bonus_id)

    class Meta:
        app_label = 'users'
        verbose_name = 'Список/База карточек'
        verbose_name_plural = 'Список/База карточек'

class User(AbstractUser):
    username = models.CharField("Имя пользователя", max_length=255)
    phone = models.CharField("Номер телефона", unique=True)
    code = models.IntegerField("Код активации", null=True, blank=True)
    activated = models.BooleanField("Активировано", default=False)
    bonus_id = models.ForeignKey(BonusCard, on_delete=models.CASCADE, null=True, blank=True, related_name='user_bonus')
    bonus = models.DecimalField("Бонус пользователя", max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    qrimg = models.ImageField("QRcode Пользователя", null=True, blank=True)
    notification = models.BooleanField("Получать уведомления", default=False)

    USERNAME_FIELD = "phone"
    objects = CustomUserManager()

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        is_new = self._state.adding

        super(User, self).save(*args, **kwargs)

        if is_new:
            bonus_id_value = BonusId.generate_bonus_id()
            bonus_id = BonusId.objects.create(bonus_id=bonus_id_value)

            bonus_card = BonusCard.objects.create(user=self, bonus_id=bonus_id)

            self.bonus_id = bonus_card

            self.code = random.randint(100000, 999999)

            qr = qrcode.make(bonus_id_value, border=2)
            qr_path = f"user/bonus-qr/{bonus_id_value}.png"
            qr.save(os.path.join(settings.MEDIA_ROOT, qr_path))
            self.qrimg.name = qr_path

            super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
