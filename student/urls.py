
from django.urls import path,include
from student import views

urlpatterns = [
    path('index/', views.index,name="stu_index"),


]
