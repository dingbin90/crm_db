from django.shortcuts import render,redirect
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from king_admin import king_admin
from django.db.models import Q
from king_admin.forms import create_model_form

# Create your views here.


def index(request):
     #king_admin.enable_admins 获取enable_admin 的数据字典里面包含{crm:{customer:admin_class}}这样类型的字典
    return render(request,'king_admin/index.html',{'table_list':king_admin.enable_admins})

def get_filter_result(request,querysets):
    filter_conditions = {}
    for key,val in request.GET.items():
        if key == "_page" or key == "_q":
            continue
        if val:
            filter_conditions[key] = val

    print(filter_conditions)
    return querysets.filter(**filter_conditions).order_by("-id"),filter_conditions

def table_search(request,admin_class,querysets):
    search_key = request.GET.get('_q','')
    print("search",search_key)
    q_obj = Q()
    q_obj.connector = "OR"
    for conlum in admin_class.list_search:
        print('conlum',conlum)
        q_obj.children.append(("%s__contains"%conlum,search_key))
    res = querysets.filter(q_obj)
    print("res",res)
    return res


def display_table_objs(request,app_name,tables_name):
    admin_class = king_admin.enable_admins[app_name][tables_name]
    querysets = admin_class.model.objects.all()
    # table_name = admin_class.model._meta.verbose_name
    querysets,filter_condtions = get_filter_result(request,querysets)
    print("!!!!!bafa",filter_condtions)

    querysets = table_search(request,admin_class,querysets)
    admin_class.filter_condtions = filter_condtions
    # print(request.GET)

    paginator = Paginator(querysets,4) #分页，每页4条数据
    page = request.GET.get('_page')

    try:
        querysets = paginator.page(page)

    except PageNotAnInteger:
        querysets = paginator.page(1)

    except EmptyPage:
        querysets = paginator.page(paginator.num_pages)


    return render(request,"king_admin/table_object.html",{'admin_class':admin_class,
                                                          'querysets':querysets,
                                                          "filter_condtions":filter_condtions,
                                                          "search_text":request.GET.get('_q',''),
                                                          }
                  )

def table_obj_change(request,app_name,tables_name,obj__id):
    admin_class = king_admin.enable_admins[app_name][tables_name]
    model_form_class = create_model_form(request,admin_class)
    obj = admin_class.model.objects.get(id=obj__id)
    if request.method == "POST":
        print('PST',request.POST)
        form_obj = model_form_class(request.POST,instance=obj)
        if form_obj.is_valid():
            form_obj.save()
    else:
        form_obj = model_form_class(instance=obj)

    return render(request,"king_admin/table_obj_change.html",{'form_obj':form_obj,
                                                              'admin_class':admin_class,
                                                              })


def table_obj_add(request,app_name,tables_name):
    admin_class = king_admin.enable_admins[app_name][tables_name]
    model_form_class = create_model_form(request, admin_class)
    if request.method == "POST":
        form_obj = model_form_class(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(request.path.replace("/add/",""))
    else:
        form_obj = model_form_class()
    return render(request,"king_admin/table_obj_add.html",{'form_obj':form_obj})

