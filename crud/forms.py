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