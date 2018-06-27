
from django.urls import path,include,re_path
from crm import views

urlpatterns = [
    re_path('^$', views.index,name="sales_index"),
    re_path('^customers/$',views.customer_list,name="customer_list"),

]
