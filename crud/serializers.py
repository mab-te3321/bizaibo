from rest_framework import serializers
from .models import *  # Import your models accordingly

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
class SolarPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarPanel
        fields = '__all__'
class InverterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inverter
        fields = '__all__'
class StructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Structure
        fields = '__all__'
class CablingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabling
        fields = '__all__'

class NetMeteringSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetMetering
        fields = '__all__'
