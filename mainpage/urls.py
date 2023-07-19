from django.urls import path
from . import views
from .models import Counties, Material, Fabricator, Statistic


urlpatterns = [
    path('', views.index),
    path('about-project', views.about),
    path('database', views.database),
    path('database-counties', views.database_info, {'model': Counties, 'title': 'Таблица уездов'}),
    path('database-materials', views.database_info, {'model': Material, 'title': 'Виды производств'}),
    path('database-fabricators', views.database_info, {'model': Fabricator, 'title': 'Список предприятий'}),
    path('database-values', views.database_info, {'model': Statistic, 'title': 'Данные по производству'}),
    path('find-manufactures', views.find_manufacture),
    path('graphics-average-revenue', views.graphics, {'graphic_type': 'Средняя выручка'}),
    path('graphics-count-workers', views.graphics, {'graphic_type': 'Число работников'}),
    path('graphics-revenue', views.graphics, {'graphic_type': 'Выручка предприятий'}),
    path('graphics-ind-power', views.graphics, {'graphic_type': 'Число индикативных сил'}),
    path('graphics-comparison', views.graphics, {'graphic_type': 'Сравнение двух предприятий'}),
    path('graphics-coefficient-revenue', views.graphics, {'graphic_type': 'Выручка на одного работника'}),
    path('graphics-coefficient-forces', views.graphics, {'graphic_type': 'Выручка на индикативную силу'}),
    path('parameters', views.graphics, {'graphic_type': 'Анализ показателей'}),
    path('entrepreneurs', views.entrepreneurs),
    path('ententrepreneurs/<int:post_id>/', views.entrepreneur_info)
]
