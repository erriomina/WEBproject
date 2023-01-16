from django.db import models

# Create your models here.
class Analytics(models.Model):
    name = models.CharField('Название профессии', default='null', max_length=50)
    demand_graph = models.ImageField('График "востребованность"', default='null')
    geography_graph = models.ImageField('График "география"', default='null')
    skills_graph = models.ImageField('График "навыки"', default='null')
    demand_table = models.FileField('Таблица "востребованность"', default='null')
    geography_table = models.FileField('Таблица "география"', default='null')
    skills_table = models.FileField('Таблица "навыки"', default='null')