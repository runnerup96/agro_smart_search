import django.forms
from django.forms import *

from .models import *



class PlantRequestForm(ModelForm):
    class Meta:
        model = PlantRequest

        fields = '__all__'

    climate = MultipleChoiceField(
        choices=[(None, 'Не выбрано')] +
                [(climate.id, climate.name) for climate in Climate.objects.all()],
        widget=CheckboxSelectMultiple(attrs={
        }))

    soil = MultipleChoiceField(
        choices=[(None, 'Не выбрано')] +
                [(soil.id, soil.name) for soil in Soil.objects.all()],
        widget=CheckboxSelectMultiple(attrs={
        }))

    daylight_hours = MultipleChoiceField(
        choices=[(None, 'Не выбрано')] +
                [(daylight_hours.id, daylight_hours.name) for daylight_hours in DaylightHours.objects.all()],
        widget=CheckboxSelectMultiple(attrs={
        }))

    pills = MultipleChoiceField(
        choices=[(None, 'Не выбрано')] +
                [(pills.id, pills.name) for pills in Pills.objects.all()],
        widget=CheckboxSelectMultiple(attrs={
        }))
