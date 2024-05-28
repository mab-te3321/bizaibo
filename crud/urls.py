from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('new/', views.index, name='base'),
    path('<str:model_name>/', views.GenericModelListView.as_view(), name='generic_list'),
    path('<str:model_name>/new/', views.GenericModelCreateView.as_view(), name='generic_create'),
    path('<str:model_name>/edit/<int:pk>/', views.GenericModelUpdateView.as_view(), name='generic_update'),
    path('<str:model_name>/delete/<int:pk>/', views.GenericModelDeleteView.as_view(), name='generic_delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)