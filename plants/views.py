from django.shortcuts import render

from .models import *
from .forms import *


def index(request):
    form = PlantRequestForm(data=request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()

            # инфа из формы
            climates = Climate.objects.filter(id__in=request.POST.getlist('climate'))
            soils = Soil.objects.filter(id__in=request.POST.getlist('soil'))
            daylight_hours = DaylightHours.objects.filter(id__in=request.POST.getlist('daylight_hours'))
            pills = Pills.objects.filter(id__in=request.POST.getlist('pills'))

            # создание списка растенийв вывод
            plants = PlantsRequestInfo.objects.create()

            # создание растений
            plant1 = PlantInfo.objects.create(name='a')
            plant1.climate.set(climates)
            plant1.soil.set(soils)
            plant1.daylight_hours.set(daylight_hours)
            plant1.pills.set(pills)

            plant2 = PlantInfo.objects.create(name='b')
            plant2.climate.set(climates)
            plant2.soil.set(soils)
            plant2.daylight_hours.set(daylight_hours)
            plant2.pills.set(pills)

            # добавление растений в список
            plants.plants.add(plant1)
            plants.plants.add(plant2)

            data = {
                'form': form,
                'plants': plants.plants.all(),
            }

            return render(request, 'plants/index.html', data)

    data = {
        'form': form,
    }

    return render(request, 'plants/index.html', data)
