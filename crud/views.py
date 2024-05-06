from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.apps import apps
from django.urls import reverse_lazy
from . import forms

class GenericModelListView(ListView):
    template_name = 'generic_list.html'
    action = 'list'
    def get_queryset(self):
        self.model = apps.get_model('crud', self.kwargs['model_name'])
        query_set = self.model.objects.all()
        print('Query set is --> ',query_set)
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.get_queryset()
        context['model_name'] = self.kwargs['model_name']
        context['field_labels'] = self.model.get_field_labels()
        return context

class GenericModelCreateView(CreateView):
    template_name = 'generic_form.html'
    action = 'ADD'
    def get_form_class(self):
        form_class_name = self.kwargs['model_name'] + 'Form'
        print('form class name is --> ',form_class_name)
        return getattr(forms, form_class_name)

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

    def get_success_url(self):
        return reverse_lazy('generic_list', kwargs={'model_name': self.kwargs['model_name']})

class GenericModelDeleteView(DeleteView):
    template_name = 'generic_confirm_delete.html'
    action = 'delete'

    def get_object(self, queryset=None):
        model = apps.get_model('crud', self.kwargs['model_name'])
        return model.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('generic_list', kwargs={'model_name': self.kwargs['model_name']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.kwargs['model_name']
        return context

