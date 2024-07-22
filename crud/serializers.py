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
class BatteriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batteries
        fields = '__all__'
class LightningArrestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = LightningArrestor
        fields = '__all__'
class InstallationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installation
        fields = '__all__'
class InvoiceSerializer(serializers.ModelSerializer):
    solar_panel = SolarPanelSerializer(read_only=True)
    inverter = InverterSerializer(read_only=True)
    structure = StructureSerializer(read_only=True)
    cabling = CablingSerializer(read_only=True)
    net_metering = NetMeteringSerializer(read_only=True)
    battery = BatteriesSerializer(read_only=True)
    lightning_arrestor = LightningArrestorSerializer(read_only=True)
    installation = InstallationSerializer(read_only=True)
    name = ClientSerializer(read_only=True)
    class Meta:
        model = Invoice
        fields = [
            'id',
            'solar_panel_quantity',
            'solar_panel_price',
            'inverter_quantity',
            'inverter_price',
            'structure_quantity',
            'structure_price',
            'cabling_quantity',
            'cabling_price',
            'net_metering_quantity',
            'net_metering_price',
            'battery_quantity',
            'battery_price',
            'lightning_arrestor_quantity',
            'lightning_arrestor_price',
            'installation_quantity',
            'installation_price',
            'discount',
            'shipping_charges',
            'status',
            'amount_paid',
            'created_at',
            'updated_at',
            'name',
            'solar_panel',
            'inverter',
            'structure',
            'cabling',
            'net_metering',
            'battery',
            'lightning_arrestor',
            'installation',
            'total'
        ]
