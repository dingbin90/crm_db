from django.contrib import admin
from django.contrib.admin import ModelAdmin
from crm import models
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','qq','source','date')
    list_filter = ('source','date')
    search_fields = ("qq","name")
    raw_id_fields = ('consult_course',"consultant")
    filter_horizontal = ("tags",)
    # list_editable = ('status')

admin.site.register(models.Customer,CustomerAdmin)
admin.site.register(models.CustomeFollowUp)
admin.site.register(models.Enrollment)
admin.site.register(models.Course)
admin.site.register(models.Class_List)
admin.site.register(models.CourseRecord)
admin.site.register(models.Branch)
admin.site.register(models.Role)
admin.site.register(models.Payment)
admin.site.register(models.StudyRecord)
admin.site.register(models.UserProfile)
admin.site.register(models.Tag)
admin.site.register(models.Menu)
admin.site.register(models.ContractTemplate)