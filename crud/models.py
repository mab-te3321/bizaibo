from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone
from django.urls import reverse
from django.utils.timezone import now

from datetime import datetime
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
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50,null=True, blank=True)
    capacity = models.CharField(max_length=50)
    price = models.FloatField(null=True, blank=True)

class Inverter(models.Model,Utility):
    name = models.CharField(max_length=100)
    choice = models.CharField(max_length=100)
    capacity = models.CharField(max_length=50)
    price = models.FloatField(null=True, blank=True)
class Structure(models.Model,Utility):
    name = models.CharField(max_length=50,null=True, blank=True)
    brand = models.CharField(max_length=100)
    price = models.FloatField(null=True, blank=True)
class Cabling(models.Model,Utility):
    name = models.CharField(max_length=100)
    price = models.FloatField(null=True, blank=True)

class NetMetering(models.Model,Utility):
    name = models.CharField(max_length=100)
    phase_type = models.CharField(max_length=50)
    price = models.FloatField(null=True, blank=True)

# Define the Invoice model incorporating fields from other models
class Invoice(models.Model, Utility):
    STATUS_CHOICES = [
        ('QUOTE', 'Quote'),
        ('PARTIALLY_PAID', 'Partially Paid'),
        ('PAID', 'Paid'),
    ]
    
    name = models.ForeignKey('Client', on_delete=models.DO_NOTHING)
    solar_panel = models.ForeignKey('SolarPanel', on_delete=models.DO_NOTHING)
    solar_panel_quantity = models.IntegerField(default=1)
    solar_panel_price = models.DecimalField(max_digits=10, decimal_places=2)

    inverter = models.ForeignKey('Inverter', on_delete=models.DO_NOTHING)
    inverter_quantity = models.IntegerField(default=1)
    inverter_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)

    structure = models.ForeignKey('Structure', on_delete=models.DO_NOTHING)
    structure_quantity = models.IntegerField(default=1)
    structure_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)

    cabling = models.ForeignKey('Cabling', on_delete=models.DO_NOTHING)
    cabling_quantity = models.IntegerField(default=1)
    cabling_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)

    net_metering = models.ForeignKey('NetMetering', on_delete=models.DO_NOTHING)
    net_metering_quantity = models.IntegerField(default=1)
    net_metering_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, help_text="Enter discount.")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='QUOTE')
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def get_download_url(self):
        """Return a URL for downloading the invoice."""
        return reverse('download-invoice', kwargs={'invoice_id': self.pk})

    def __str__(self):
        return f"Invoice {self.id} - {self.name.name}"

    def save(self, *args, **kwargs):
        if not self.pk:  # If new instance
            # Set default prices from related models
            self.solar_panel_price = self.solar_panel.price
            self.inverter_price = self.inverter.price
            self.structure_price = self.structure.price
            self.cabling_price = self.cabling.price
            self.net_metering_price = self.net_metering.price
        super().save(*args, **kwargs)