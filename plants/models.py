from django.db import models


class Soil(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тип почвы'
        verbose_name_plural = 'Типы почвы'

    def __str__(self):
        return self.name


class Climate(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тип климата'
        verbose_name_plural = 'Типы климата'

    def __str__(self):
        return self.name


class Pills(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Препарат'
        verbose_name_plural = 'Препараты'

    def __str__(self):
        return self.name


class DaylightHours(models.Model):
    name = models.CharField(max_length=100, verbose_name='Время суток')

    class Meta:
        verbose_name = 'Световой день'
        verbose_name_plural = 'Световые дни'

    def __str__(self):
        return self.name


class PlantInfo(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', blank=True)
    sowing_period = models.CharField(max_length=100, verbose_name='Период посева', blank=True, null=True)
    harvest_period = models.CharField(max_length=100, verbose_name='Период сбора', blank=True, null=True)
    chemical_composition = models.TextField(verbose_name='Химический состав', blank=True, null=True)
    medical_preparations = models.TextField(verbose_name='Лекарственные препараты', blank=True, null=True)
    raw_material_need = models.PositiveIntegerField(verbose_name='Количество необходимого сырья (тонны)', blank=True, null=True)
    in_red_book = models.BooleanField(verbose_name='В красной книге', blank=True, null=True)
    region_red_book = models.CharField(max_length=100, verbose_name='Регион в красной книге', blank=True, null=True)

    climate = models.ManyToManyField(Climate, verbose_name='Типы климата', blank=True, null=True)
    soil = models.ManyToManyField(Soil, verbose_name='Типы почвы', blank=True, null=True)
    daylight_hours = models.ManyToManyField(DaylightHours, verbose_name='Световой день', blank=True, null=True)
    pills = models.ManyToManyField(Pills, verbose_name='Препараты', blank=True, null=True)

    class Meta:
        verbose_name = 'Информация о растении'
        verbose_name_plural = 'Информация о растениях'

    def __str__(self):
        return self.name


class PlantsRequestInfo(models.Model):
    plants = models.ManyToManyField(PlantInfo, verbose_name='Растения', blank=True)

    class Meta:
        verbose_name = 'Информация о запросе на растения'
        verbose_name_plural = 'Информация о запросах на растения'

    def __str__(self):
        names = [plant.name for plant in self.plants.all()]
        return ', '.join(names)


class PlantRequest(models.Model):
    climate = models.ManyToManyField(Climate, verbose_name='Типы климата', blank=True)
    soil = models.ManyToManyField(Soil, verbose_name='Типы почвы', blank=True)
    daylight_hours = models.ManyToManyField(DaylightHours, verbose_name='Световой день', blank=True)
    pills = models.ManyToManyField(Pills, verbose_name='Препараты', blank=True)

    class Meta:
        verbose_name = 'Запрос на растение'
        verbose_name_plural = 'Запросы на растения'

    def __str__(self):
        return f'{self.id}'
