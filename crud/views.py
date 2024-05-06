from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import MyModel
from .forms import MyModelForm

class MyModelListView(ListView):
    model = MyModel
    context_object_name = 'items'
    template_name = 'my_model_list.html'

class MyModelCreateView(CreateView):
    model = MyModel
    form_class = MyModelForm
    success_url = reverse_lazy('my_model_list')
    template_name = 'my_model_form.html'

class MyModelUpdateView(UpdateView):
    model = MyModel
    form_class = MyModelForm
    success_url = reverse_lazy('my_model_list')
    template_name = 'my_model_form.html'

class MyModelDeleteView(DeleteView):
    model = MyModel
    success_url = reverse_lazy('my_model_list')
    template_name = 'my_model_confirm_delete.html'
