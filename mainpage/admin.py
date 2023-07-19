from django.contrib import admin
from .models import Counties, Material, Fabricator, Statistic


admin.site.register(Counties)
admin.site.register(Material)
admin.site.register(Fabricator)
admin.site.register(Statistic)