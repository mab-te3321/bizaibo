from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.apps import apps
from django.urls import reverse_lazy
from . import forms
from .models import *
from rest_framework import serializers
from rest_framework import viewsets
from django.db.models import Q
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def index(request):
	posts = Invoice.objects.all() # fetching all post objects from database
	p = Paginator(posts, 1) # creating a paginator object
	# getting the desired page number from url
	page_number = request.GET.get('page')
	try:
		page_obj = p.get_page(page_number) # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = p.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = p.page(p.num_pages)
	context = {'page_obj': page_obj}
	# sending the page object to index.html
	return render(request, 'index.html', context)

#edited by B C SAMRUDH

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
        if search_query:
            query = Q()
            for field in self.get_searchable_fields():
                query |= Q(**{f"{field}__icontains": search_query})
            queryset = queryset.filter(query)
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