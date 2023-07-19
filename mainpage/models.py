from django.db import models


class Counties(models.Model):
    county_name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.county_name


class Material(models.Model):
    material_name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.material_name


class Fabricator(models.Model):
    county_name = models.ForeignKey(Counties, on_delete=models.CASCADE)
    material_name = models.ForeignKey(Material, on_delete=models.CASCADE)
    fabricator_name = models.CharField(max_length=50, null=False)
    location = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.fabricator_name


class Statistic(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, null=False)
    county = models.ForeignKey(Counties, on_delete=models.CASCADE, null=False)
    fabricator = models.ForeignKey(Fabricator, on_delete=models.CASCADE, null=False)
    revenue = models.FloatField()
    indicative_forces = models.FloatField()
    workers = models.IntegerField()
    info = models.CharField(max_length=2000, null=True)
    photo = models.CharField(max_length=100, null=True)
