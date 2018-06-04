from django import template
from django.utils.safestring import mark_safe
import datetime,time
register = template.Library()
@register.simple_tag
def render_app_name(admin_class):
    return admin_class.model._meta.verbose_name

@register.simple_tag
def get_query_sets(admin_class):
    return admin_class.model.objects.all()


@register.simple_tag
def build_table_row(request,obj,admin_class):
    row_ele = ""
    for index,column in enumerate(admin_class.list_display):
        print('index',index,column,request.path)
        filed_obj = obj._meta.get_field(column) #获取字段类型
        if filed_obj.choices: #判断字段类型是choice的
            column_data = getattr(obj,"get_%s_display"%column)() #获取choice类型的数据
        else:
            column_data = getattr(obj,column) #获取其他类型的数据
        if index == 0 :  #add tag ,可以跳转到修改页
            column_data = "<a href='{request_path}/{obj_id}/change'>{data}</a>".format(request_path=request.path,
                                                                                       obj_id=obj.id,
                                                                                       data=column_data)

        row_ele += "<td>%s</td>" %column_data
    return  mark_safe(row_ele)

@register.simple_tag
def build_filter_ele(filter_column,admin_class):
    filter_ele = "<select name='%s'>" % filter_column  #选择框
    column_obj = admin_class.model._meta.get_field(filter_column)#获取过滤字段的对象
    try:
        for choice in column_obj.get_choices(): #获取过滤字段的内容，是一个元组，
            select = 'selected'
            if filter_column in admin_class.filter_condtions:
                # print("@@@@",type(admin_class.filter_condtions.get(filter_column)))
                # print("####",type(choice[0]))
                if str(choice[0]) == admin_class.filter_condtions.get(filter_column):
                    # selected = 'selected'
                    print("$$$$$")
                    option = "<option value='%s' %s > %s </option>" % (choice[0],select,choice[1])
                else:
                    selected = ''
                    option = "<option value='%s' '%s' > %s </option>" % (choice[0], selected, choice[1])
            else:
                 selected = ''
                 option = "<option value='%s' '%s' > %s </option>" % (choice[0],selected,choice[1])
            # print("selected",selected)
            filter_ele += option
    except AttributeError as e:  #date类型的字段要额外的判断，不然会抛出异常
        print("err",e)
        if column_obj.get_internal_type() in ('DateField','DateTimeField'): #判断字段类型是不是属于之中
            time_obj = datetime.datetime.now() #获取当前的时间
            time_list =[
                ['','--------'],
                [time_obj, 'Today'],
                [time_obj-datetime.timedelta(7),'七天内'],
                [time_obj.replace(day=1),'本月'],
                [time_obj-datetime.timedelta(90),'三个月内'],
                [time_obj.replace(month=1,day=1),'YearToDay()YTD'],
                ['','ALL'],
            ]
            for i in time_list:
                option = "<option value='%s'> %s </option>" %(i[0],i[1])
                filter_ele +=option


    filter_ele += "</select>"
    # print(filter_ele)
    return mark_safe(filter_ele)
@register.simple_tag
def render_paginator(querysets):
    ele = '''
            <ul class="pagination">
             <li class=""><a href="#" >&laquo</a></li>
    '''
    if querysets.has_previous():
        ele = '''     
        <ul class="pagination">        
        <li class=""><a href="?_page=%s" >&laquo</a></li>
         ''' % querysets.previous_page_number()


    for i in querysets.paginator.page_range:

        if abs(querysets.number - i) < 2:
            active = ''
            if querysets.number == i :
                active = 'active'
            p_ele = '''
            <li class="%s"><a href="?_page=%s">%s </a></li>    

            ''' % (active,i,i)
            ele += p_ele

    ele += '</ul>'

    return mark_safe(ele)

@register.simple_tag
def get_model_name(admin_class):
    return admin_class.model._meta.verbose_name

@register.simple_tag
def get_m2m_obj_list(admin_class,field,form_obj):
    '''返回m2m待选数据'''
    field_obj = getattr(admin_class.model,field.name)
    all_obj_list = field_obj.rel.model.objects.all()
    obj_instance_list = getattr(form_obj.instance,field.name)

    selected_obj_list = obj_instance_list.all()
    standby_obj_list = []
    for obj in all_obj_list:
        if obj not in selected_obj_list:
            standby_obj_list.append(obj)

    return standby_obj_list


@register.simple_tag
def get_m2m_selected_obj_list(form_obj,field):
    '''返回以选择的数据'''
    field_obj = getattr(form_obj.instance,field.name)
    return field_obj.all()