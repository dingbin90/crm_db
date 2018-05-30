
from django.urls import path,include,re_path
from king_admin import views

urlpatterns = [
    re_path('^$', views.index,name="table_index"),
    re_path(r'^(\w+)/(\w+)$',views.display_table_objs,name="table_jj"),


]
