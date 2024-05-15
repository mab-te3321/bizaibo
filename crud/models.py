from django.db import models
from django.forms.models import model_to_dict
class Utility():
    @classmethod
    def get_field_labels(cls):
        # Returns a list of tuples (field name, field label)
        res = [(field.name, field.verbose_name) for field in cls._meta.fields]
        print(f"Meta Fields are {cls._meta.fields}")
        print(f"Res is {res}")
        return res

class Client(models.Model,Utility):
    cnic = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100,help_text="You Area (i.e DHA, Gulberg, etc.)")
    contract_number = models.CharField(max_length=20)
    monthly_consumption_units = models.IntegerField(null=True,help_text="Monthly consumption in units")
class SolarPanel(models.Model,Utility):
    brand = models.CharField(max_length=100)
    type = models.CharField(max_length=50,null=True, blank=True)
    capacity = models.CharField(max_length=50)
    price = models.FloatField(null=True, blank=True)

class Inverter(models.Model,Utility):
    brand = models.CharField(max_length=100)
    choice = models.CharField(max_length=100)
    capacity = models.CharField(max_length=50)
    price = models.FloatField(null=True, blank=True)
class Structure(models.Model,Utility):
    type = models.CharField(max_length=50,null=True, blank=True)
    brand = models.CharField(max_length=100)
    price = models.FloatField(null=True, blank=True)
class Cabling(models.Model,Utility):
    brand = models.CharField(max_length=100)
    price = models.FloatField(null=True, blank=True)

class NetMetering(models.Model,Utility):
    name = models.CharField(max_length=100)
    phase_type = models.CharField(max_length=50)
    price = models.FloatField(null=True, blank=True)

# Define the Invoice model incorporating fields from other models
class Invoice(models.Model,Utility):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    solar_panel = models.ForeignKey(SolarPanel, on_delete=models.DO_NOTHING)
    inverter = models.ForeignKey(Inverter, on_delete=models.DO_NOTHING)
    structure = models.ForeignKey(Structure, on_delete=models.DO_NOTHING)
    cabling = models.ForeignKey(Cabling, on_delete=models.DO_NOTHING)
    net_metering = models.ForeignKey(NetMetering, on_delete=models.DO_NOTHING)
    