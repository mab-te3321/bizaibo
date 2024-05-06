from django.shortcuts import render, redirect
from .models import MyModel
from .forms import MyModelForm

def model_list(request):
    items = MyModel.objects.all()
    return render(request, 'model_list.html', {'items': items})

def model_create(request):
    if request.method == "POST":
        form = MyModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('model_list')
    else:
        form = MyModelForm()
    return render(request, 'model_form.html', {'form': form})

def model_update(request, id):
    item = MyModel.objects.get(id=id)
    if request.method == "POST":
        form = MyModelForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('model_list')
    else:
        form = MyModelForm(instance=item)
    return render(request, 'model_form.html', {'form': form})

def model_delete(request, id):
    item = MyModel.objects.get(id=id)
    if request.method == "POST":
        item.delete()
        return redirect('model_list')
    return render(request, 'model_confirm_delete.html', {'object': item})
