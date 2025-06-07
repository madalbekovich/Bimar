from django.db import models
from apps.users.models import User
from ckeditor.fields import RichTextField
from babel.dates import format_date

class Story(models.Model):
    created_at = models.DateTimeField("Дата и время", auto_now_add=True)
    img = models.ImageField("Изображение", upload_to="story_images")
    link = models.URLField('Ссылка', max_length=500, blank=True, null=True, help_text='Если есть')
    title = models.CharField('Заголовок истории', max_length=255)

    class Meta:
        verbose_name = "История"
        verbose_name_plural = "Истории"

class StoryVideo(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="stories")
    url = models.FileField("История", upload_to="stories")
    created_at = models.DateTimeField("Дата и время", auto_now_add=True)

    class Meta:
        verbose_name = "История"
        verbose_name_plural = "Истории"

    def __str__(self):
        return self.created_at.strftime("%d %B %Y г. %H:%M")

class Notification(models.Model):
    user_id = models.ManyToManyField(
        "DeviceToken",
        blank=True,
        verbose_name="Кому отправить?",
        help_text="**Если хотите уведомить всех, оставьте это поле пустым**"
    )
    sendtoall = models.BooleanField(default=True, verbose_name="Отправить всем")
    title = models.CharField('Уведомление', max_length=255)
    description = models.TextField("Описание", blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    big_img = models.ImageField(
        "Оболожка",
        upload_to='notifications/%Y_%m',
        null=True,
        blank=True,
        help_text="Большое фото товара для магазина, обложка новости, рекламный баннер или иллюстрация к событию."
    )
    large_img = models.ImageField(
        "Значок акции",
        upload_to='notifications/%Y_%m',
        null=True,
        blank=True,
        help_text="Тематическая иконка, связанная с содержимым уведомления (например, значок акции или события)."
    )

    class Meta:
        verbose_name = 'Уведомления'
        verbose_name_plural = 'Уведомлении'


class DeviceToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    device_token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}."

class News(models.Model):
    img = models.ImageField(upload_to='news/', verbose_name='Изображение')
    title = models.CharField(max_length=100, verbose_name='Название')
    description = RichTextField(verbose_name='Описание')
    date = models.DateField(null=True, blank=True, verbose_name='Дата назначение')
    date_appointment = models.CharField(null=True, blank=True, editable=False)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def save(self, *args, **kwargs):
        if self.date:
            self.date_appointment = format_date(self.date, format='d MMMM', locale='ru')
        else:
            self.date_appointment = ''
        super().save(*args, **kwargs)


class StoreBranch(models.Model):
    address = models.CharField(verbose_name='Адрес филиала')

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

    def __str__(self):
        return self.address

