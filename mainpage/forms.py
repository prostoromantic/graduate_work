from django import forms
from .models import Statistic


class ParameterForm(forms.Form):
    OPTIONS = (
        ('revenue', 'Выручка'),
        ('workers_count', 'Количество работников'),
        ('indicative_forces', 'Число индикативных сил'),
    )
    parameters = forms.CharField(widget=forms.RadioSelect(choices=tuple(OPTIONS)))


class FabricatorForm(forms.Form):
    values = Statistic.objects.all()
    OPTIONS = []
    for value in values:
        OPTIONS.append((value.id, value.fabricator.fabricator_name,))
    fabricator = forms.CharField(widget=forms.Select(choices=tuple(OPTIONS)))