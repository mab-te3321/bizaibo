from django.urls import path
from . import views

urlpatterns = [
    path('<str:model_name>/', views.GenericModelListView.as_view(), name='generic_list'),
    path('<str:model_name>/new/', views.GenericModelCreateView.as_view(), name='generic_create'),
    path('<str:model_name>/edit/<int:pk>/', views.GenericModelUpdateView.as_view(), name='generic_update'),
    path('<str:model_name>/delete/<int:pk>/', views.GenericModelDeleteView.as_view(), name='generic_delete'),
]
