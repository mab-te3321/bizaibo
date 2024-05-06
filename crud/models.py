from django.db import models
from django.forms.models import model_to_dict
class Utility():
    @classmethod
    def get_field_labels(cls):
        # Returns a list of tuples (field name, field label)
        return [(field.name, field.verbose_name) for field in cls._meta.fields]

class Client(models.Model,Utility):
    cnic = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    area = models.FloatField(help_text="Area in square meters")
    contract_number = models.CharField(max_length=20)
    monthly_consumption_units = models.IntegerField(help_text="Monthly consumption in units")
class SolarPanel(models.Model,Utility):
    brand = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    capacity = models.CharField(max_length=50)
    price = models.FloatField()

class Inverter(models.Model,Utility):
    brand = models.CharField(max_length=100)
    choice = models.CharField(max_length=100)
    capacity = models.CharField(max_length=50)
    price = models.FloatField()
class Structure(models.Model,Utility):
    l2 = models.CharField(max_length=100, blank=True, null=True)  # Assuming L2/L3 are types of structures
    l3 = models.CharField(max_length=100, blank=True, null=True)
    h_beam = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.FloatField()
class Cabling(models.Model,Utility):
    brand = models.CharField(max_length=100)

class NetMetering(models.Model,Utility):
    name = models.CharField(max_length=100)
    phase_type = models.CharField(max_length=50)
