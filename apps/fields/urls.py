from django.urls import path
from apps.fields import views

urlpatterns = [
    path('create/', views.create_field, name='create_field'),
    path('<int:pk>/update/', views.update_field, name='update_field'),
    path('<int:pk>/delete/', views.delete_field, name='delete_field'),
    path('', views.get_fields, name='get_fields'),
    path('field/<int:pk>', views.get_field, name='get_field'),
]