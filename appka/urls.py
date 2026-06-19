from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("orders/", views.orders, name="orders"),
    path("customers/", views.customers, name="customers"),
    path("customers/<int:pk>/", views.customer_detail, name="customer_detail"),
    path("employees/", views.employees, name="employees"),
    path("stats/", views.stats, name="stats"),
]