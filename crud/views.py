from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.apps import apps
from django.urls import reverse_lazy
from . import forms
from .models import *
from .serializers import *
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from django.http import HttpResponse
from crud.task import add 
import importlib
from rest_framework.exceptions import NotFound
from django.conf import settings
from django.http import FileResponse
import os
from django.http import Http404
class DynamicModelViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        model_name = self.kwargs['model_name']
        try:
            model = apps.get_model('crud', model_name)
        except LookupError:
            raise NotFound(f"Model '{model_name}' not found.")
        return model.objects.all()

    def get_serializer_class(self):
        model_name = self.kwargs['model_name']
        module_path = 'crud.serializers'
        serializer_class_name = model_name + 'Serializer'

        try:
            serializers_module = importlib.import_module(module_path)
            serializer_class = getattr(serializers_module, serializer_class_name)
        except (ImportError, AttributeError):
            raise NotFound(f"Serializer for model '{model_name}' not found.")
        
        return serializer_class

def index(request):
    file_path = os.path.join(settings.BASE_DIR, 'test.rest')  # Update this to the path of your file

    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='test.rest')  # 'as_attachment=True' makes it a download
    else:
        raise Http404("File not found.")
def modify_and_send_file(request, invoice_id):
    try:
        invoice = Invoice.objects.get(pk=invoice_id)
        file_path = r'edited_example.docx'
    except Invoice.DoesNotExist:
        raise Http404("Invoice not found.")

    # Ensure the file exists
    if not os.path.exists(file_path):
        raise Http404("File not found.")

    # Read and modify the file
    # modified_file_path = os.path.join(settings.MEDIA_ROOT, 'temp', f'modified_{invoice.id}.pdf')
    # with open(file_path, 'rb') as file:
    #     content = file.read()
    #     # Modify your content here, this is just a placeholder
    #     modified_content = content.replace(b'Original', b'Modified')

    # # Write to a temporary file
    # with open(modified_file_path, 'wb') as temp_file:
    #     temp_file.write(modified_content)

    # Send the file
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f'modified_invoice_{invoice.id}.docx')

class GenericModelListView(ListView):
    template_name = 'generic_list.html'
    action = 'list'
    paginate_by = 5
    models = ['Client', 'SolarPanel', 'Inverter', 'Structure', 'Cabling', 'NetMetering', 'Invoice']
    
    def get_queryset(self):
        self.model = apps.get_model('crud', self.kwargs['model_name'])
        queryset = self.model.objects.all()
        queryset = self.apply_filters(queryset)
        queryset = self.apply_sort(queryset)
        return queryset
    
    def apply_filters(self, queryset):
        search_query = self.request.GET.get('q')
        date_range = self.request.GET.get('date_range')
        if search_query:
            query = Q()
            for field in self.get_searchable_fields():
                query |= Q(**{f"{field}__icontains": search_query})
            queryset = queryset.filter(query)
        if date_range:
            try:
                start_date, end_date = date_range.split(' to ')
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                queryset = queryset.filter(created_at__range=(start_date, end_date))
            except ValueError:
                pass
        return queryset

    def get_searchable_fields(self):
        fields = []
        for field in self.model._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                fields.append(field.name)
            elif isinstance(field, models.ForeignKey):
                # Adjust the search to use 'name' or 'brand' for ForeignKey fields
                if hasattr(field.related_model, 'name'):
                    fields.append(f"{field.name}__name")
                elif hasattr(field.related_model, 'brand'):
                    fields.append(f"{field.name}__brand")
        return fields

    def apply_sort(self, queryset):
        sort_by = self.request.GET.get('sort_by', None)
        if sort_by:
            if sort_by.startswith('-'):
                sort_by = sort_by[1:]
            else:
                sort_by = f'-{sort_by}'
            queryset = queryset.order_by(sort_by)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.kwargs['model_name']
        context['field_labels'] = self.model.get_field_labels()
        return context

class GenericModelCreateView(CreateView):
    template_name = 'generic_form.html'
    action = 'ADD'
    
    def get_form_class(self):
        model_name = self.kwargs['model_name']
        form_class_name = self.kwargs['model_name'] + 'Form'
        print('form class name is --> ',form_class_name)
        return getattr(forms, form_class_name)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({'files': self.request.FILES})
        return kwargs
    def get_context_data(self, **kwargs):
        context = super(GenericModelCreateView, self).get_context_data(**kwargs)
        context['model_name'] = self.kwargs.get('model_name', 'InvoiceModel')
        context['action'] = self.action
        return context
    def get_success_url(self):
        return reverse_lazy('generic_list', kwargs={'model_name': self.kwargs['model_name']})
        

class GenericModelUpdateView(UpdateView):
    template_name = 'generic_form.html'
    action = 'update'
    def get_object(self, queryset=None):
        model = apps.get_model('crud', self.kwargs['model_name'])
        return model.objects.get(pk=self.kwargs['pk'])

    def get_form_class(self):
        form_class_name = self.kwargs['model_name'] + 'Form'
        return getattr(forms, form_class_name)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({'files': self.request.FILES})
        return kwargs
    def get_context_data(self, **kwargs):
        context = super(GenericModelUpdateView, self).get_context_data(**kwargs)
        context['model_name'] = self.kwargs.get('model_name', 'InvoiceModel')
        context['action'] = self.action
        return context
    def get_success_url(self):  
        return reverse_lazy('generic_list', kwargs={'model_name': self.kwargs['model_name']})

class GenericModelDeleteView(DeleteView):
    template_name = 'generic_confirm_delete.html'
    action = 'delete'
    def get_context_data(self, **kwargs):
        context = super(GenericModelDeleteView, self).get_context_data(**kwargs)
        context['model_name'] = self.kwargs.get('model_name', 'InvoiceModel')
        context['action'] = self.action
        return context
    def get_object(self, queryset=None):
        model = apps.get_model('crud', self.kwargs['model_name'])
        return model.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('generic_list', kwargs={'model_name': self.kwargs['model_name']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.kwargs['model_name']
        return context

    """
    A ViewSet that determines the queryset and serializer class dynamically
    based on the 'model_name' URL keyword argument.
    """

    def get_queryset(self):
        model_name = self.kwargs.get('model_name')
        if model_name:
            model = apps.get_model('crud', model_name)
            return model.objects.all()
        else:
            raise ImproperlyConfigured("No model specified!")

    def get_serializer_class(self):
        model_name = self.kwargs.get('model_name')
        if model_name:
            class Meta:
                model = apps.get_model('crud', model_name)
                model = model
                fields = '__all__'

            serializer_class = type(
                f"{model_name}Serializer",
                (serializers.ModelSerializer,),
                {'Meta': Meta}
            )
            return serializer_class
        else:
            raise ImproperlyConfigured("No model specified!")