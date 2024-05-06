from django.urls import path
from . import views

urlpatterns = [
    path('', views.model_list, name='model_list'),
    path('new/', views.model_create, name='model_create'),
    path('edit/<int:id>/', views.model_update, name='model_update'),
    path('delete/<int:id>/', views.model_delete, name='model_delete'),
]
