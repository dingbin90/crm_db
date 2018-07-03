from django.shortcuts import render
from crm import forms
from crm import models
from django.db import IntegrityError
import random,string
from django.core.cache import cache
# Create your views here.


def index(request):
    return render(request,"index.html")


def customer_list(request):
    return render(request,"sales/customers.html")



def stu_registration(request,enroll_id,random_str):
    enroll_obj = models.Enrollment.objects.get(id=enroll_id)
    if request.method == "POST":
        customer_form = forms.CustomerForm(request.POST,instance=enroll_obj.customer)
        if customer_form.is_valid():
            customer_form.save()
            enroll_obj.contract_agree = True
            enroll_obj.save()
            return render(request, "sales/stu_registration.html", {"status": 1})
    else:
        if enroll_obj.contract_agree == True:
            status = 1
        else:
            status = 0

        customer_form = forms.CustomerForm(instance=enroll_obj.customer)

    return render(request,'sales/stu_registration.html',{'customer_form':customer_form,
                                                         'enroll_obj':enroll_obj,
                                                         'status':status,
                                                         })


def enrollment(request,customer_id):
    customer_obj = models.Customer.objects.get(id=customer_id)
    msgs = {}
    if request.method == "POST":
        # msg = '''请将此连接发给客户填写http://127.0.0.1:8000/crm/customer/enrollment/{enroll_obj_id}'''
        enroll_form = forms.EnrollmentForm(request.POST)
        if enroll_form.is_valid():
            msg = '''请将此连接发给客户填写http://127.0.0.1:8000/crm/customer/registration/{enroll_obj_id}/{random_str}/'''
            random_str = ''.join(random.sample(string.ascii_lowercase + string.digits, 8))

            try:
                enroll_form.cleaned_data["customer"] = customer_obj
                enroll_obj = models.Enrollment.objects.create(**enroll_form.cleaned_data)
                cache.set(enroll_obj.id, random_str, 3000)
                msgs['msg'] = msg.format(enroll_obj_id=enroll_obj.id,random_str=random_str)

            except IntegrityError as e:
                enroll_obj = models.Enrollment.objects.get(customer_id=customer_obj.id,
                                                           enrolled_class_id=enroll_form.cleaned_data["enrolled_class"].id)
                enroll_form.add_error("__all__","该用户的此条报名信息已存在，不能重复创建")
                # random_str = ''.join(random.sample(string.ascii_lowercase+string.digits,8))
                cache.set(enroll_obj.id,random_str,3000)
                msgs['msg'] = msg.format(enroll_obj_id=enroll_obj.id,random_str=random_str)
    else:
        enroll_form = forms.EnrollmentForm()



    return render(request,'sales/enrollment.html',{'enroll_form':enroll_form,
                                                   'customer_obj':customer_obj,
                                                   'msgs':msgs,

                                                   })

