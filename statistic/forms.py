from django import forms
from .models import Miner


class CalculateForm(forms.Form):
    miners = forms.ModelMultipleChoiceField(label='Майнеры', queryset=Miner.objects.all())
    begin_time = forms.DateTimeField(label='Время начала', input_formats=['%d/%m/%Y %H:%M'])
    end_time = forms.DateTimeField(label='Время конца', input_formats=['%d/%m/%Y %H:%M'])
    balance = forms.FloatField(label='Баланс', required=False)
