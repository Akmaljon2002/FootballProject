from django.urls import path
from apps.orders import views

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('<int:pk>/update/', views.update_order, name='update_order'),
    path('<int:pk>/delete/', views.delete_order, name='delete_order'),
    path('', views.get_orders, name='get_orders'),
    path('order/<int:pk>', views.get_order, name='get_order'),
    path('order/accept/<int:pk>', views.accept_order, name='order_accept'),
]