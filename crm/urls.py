
from django.urls import path,include
from crm import views

urlpatterns = [
    path('index/', views.index,name="sales_index"),
    path('customers/',views.customer_list,name="customer_list"),

]
