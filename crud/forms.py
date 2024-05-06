from django import forms
from .models import *

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'  # This will include all fields from the Client model.

class SolarPanelForm(forms.ModelForm):
    class Meta:
        model = SolarPanel
        fields = '__all__'

class InverterForm(forms.ModelForm):
    class Meta:
        model = Inverter
        fields = '__all__'

class StructureForm(forms.ModelForm):
    class Meta:
        model = Structure
        fields = '__all__'

class CablingForm(forms.ModelForm):
    class Meta:
        model = Cabling
        fields = '__all__'

class NetMeteringForm(forms.ModelForm):
    class Meta:
        model = NetMetering
        fields = '__all__'
class InvoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get all instances for each related model
        client_choices = [(client.pk, str(client.name)) for client in Client.objects.all()]
        solar_panel_choices = [(solar_panel.pk, str(solar_panel.brand)) for solar_panel in SolarPanel.objects.all()]
        inverter_choices = [(inverter.pk, str(inverter.brand)) for inverter in Inverter.objects.all()]
        structure_choices = [(structure.pk, str(structure.brand)) for structure in Structure.objects.all()]
        cabling_choices = [(cabling.pk, str(cabling.brand)) for cabling in Cabling.objects.all()]
        net_metering_choices = [(net_metering.pk, str(net_metering.name)) for net_metering in NetMetering.objects.all()]

        # Update choices for each ForeignKey field
        self.fields['client'].choices = client_choices
        self.fields['solar_panel'].choices = solar_panel_choices
        self.fields['inverter'].choices = inverter_choices
        self.fields['structure'].choices = structure_choices
        self.fields['cabling'].choices = cabling_choices
        self.fields['net_metering'].choices = net_metering_choices

    class Meta:
        model = Invoice
        fields = '__all__'
        