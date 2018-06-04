from crm import models
enable_admins = {}

class BaseAdmin(object):
    list_display = []
    list_filter = []
    list_search = []
    filter_horizontal = []
class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ['customer','consultant','date']
    list_search = ['customer__qq','customer__name']
    list_filter = ['customer','date','consultant']
    filter_horizontal = ['']
class CustomerAdmin(BaseAdmin):
    list_display = ['id','qq','name','source','consult_course']
    list_filter = ['source','date','consult_course']
    list_search = ['qq','name']
    filter_horizontal = ['tags']
    #model = models.Customer 等同于 admin_class.model = model_class 绑定model   与 model_class对象

def register(model_class,admin_class=None):
    if model_class._meta.app_label not in enable_admins:
        enable_admins[model_class._meta.app_label] = {}
    admin_class.model = model_class
    enable_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class


register(models.Customer,CustomerAdmin)
register(models.CustomeFollowUp,CustomerFollowUpAdmin)





