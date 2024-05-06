from django import forms
from .models import MyModel
from .models import StructureModel

class MyModelForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['name', 'description']

class StructureModelForm(forms.ModelForm):
    class Meta:
        model = StructureModel
        fields = ['length', 'width']