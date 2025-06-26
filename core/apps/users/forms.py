from django import forms

class GenerateBonusCardsForm(forms.Form):
    count = forms.IntegerField(
        label="Количество карточек",
        min_value=1,
        max_value=1000,
        initial=20,
        help_text="Введите количество бонусных карточек для создания (1–1000)."
    )
