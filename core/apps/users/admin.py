from django.contrib import admin
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from admin_extra_buttons.mixins import ExtraButtonsMixin
from admin_extra_buttons.decorators import button
from . import models
import openpyxl
from .forms import GenerateBonusCardsForm
from django.contrib.auth.admin import UserAdmin

admin.site.register(models.BonusCard)



@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('phone', 'username')
        }),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Бонусы и QR', {
            'fields': ('bonus_id', 'bonus', 'qrimg')
        }),
        ('Активация и уведомления', {
            'fields': ('code', 'activated', 'notification')
        }),
        ('Источник и ID', {
            'fields': ('registration_source', 'external_id_1c')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Даты', {
            'fields': ('last_login',)
        }),
    )

class BonusIdExtraAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ['bonus_id']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @admin.action(description="Создать бонусные карточки")
    def create_cards(self, request):
        if request.method == "POST":
            form = GenerateBonusCardsForm(request.POST)
            if form.is_valid():
                count = form.cleaned_data['count']
                try:
                    with transaction.atomic():
                        for _ in range(count):
                            bonus_id_value = models.BonusId.generate_bonus_id()
                            bonus_id = models.BonusId.objects.create(bonus_id=bonus_id_value)
                            models.BonusCard.objects.create(bonus_id=bonus_id, user=None)
                        self.message_user(request, f"Успешно создано {count} бонусных карточек.")
                        return HttpResponseRedirect('/admin/users/bonusid/')
                except Exception as e:
                    self.message_user(request, f"Ошибка при создании карточек: {str(e)}", level='error')
        else:
            form = GenerateBonusCardsForm()

        return render(request, 'admin/generate_bonus_cards.html', {
            'form': form,
            'title': 'Создать бонусные карточки',
            'app_label': 'users',
            'site_header': admin.site.site_header,
            'site_title': admin.site.site_title,
        })

    @button(
        permission="users.add_bonusid",
        change_form=False,
        change_list=True,
        html_attrs={"class": "aeb-green"},
        label="Создать бонусные карточки"
    )
    def create_cards_button(self, request):
        return self.create_cards(request)

    @admin.action(description="Экспорт бонусных ID в Excel")
    def export_to_excel(self, request):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Bonus IDs"
        headers = ['bonus_id']
        ws.append(headers)
        for bonus_id_obj in models.BonusId.objects.all():
            ws.append([bonus_id_obj.bonus_id])
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=bonus_ids_bimar.xlsx'
        wb.save(response)
        return response

    @button(
        permission="users.view_bonusid",
        change_form=False,
        change_list=True,
        html_attrs={"class": "aeb-green"},
        label="Экспорт в Excel"
    )
    def export_to_excel_button(self, request):
        return self.export_to_excel(request)

admin.site.register(models.BonusId, BonusIdExtraAdmin)
