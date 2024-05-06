from django.urls import path
from .views import MyModelListView, MyModelCreateView, MyModelUpdateView, MyModelDeleteView

urlpatterns = [
    path('', MyModelListView.as_view(), name='my_model_list'),
    path('new/', MyModelCreateView.as_view(), name='my_model_create'),
    path('edit/<int:pk>/', MyModelUpdateView.as_view(), name='my_model_update'),
    path('delete/<int:pk>/', MyModelDeleteView.as_view(), name='my_model_delete'),
]
