from django.forms import forms,ModelForm,ValidationError
from django.utils.translation import ugettext as _


def create_model_form(request,admin_class):
    '''动态生成MODEL FORM'''
    def __new__(cls,*args,**kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class']='form-control'
            if not hasattr(admin_class,'add_form'):
                if field_name in admin_class.readonly_filed:
                    field_obj.widget.attrs['disabled'] = 'disabled'
        return ModelForm.__new__(cls)

    error_list=[]
    def default_clean(self):
        if self.instance.id:#这个是表单的修改
            for field in admin_class.readonly_filed:
                field_val = getattr(self.instance,field)  #数据库的值
                field_val_from_fronted = self.cleaned_data.get(field)  #修改的值
                if field_val != field_val_from_fronted:
                    error_list.append(ValidationError(
                                    _('Field %(field)s is readonly,data should be %(val)s'),
                                    code='invalid',
                                    params={'field': field,'val':field_val},
                               ))
        # readonly_table check
        if admin_class.readonly_table:
                raise ValidationError(
                    _('Table is  readonly,cannot be modified or added'),
                    code='invalid'
                )

        self.ValidationError = ValidationError
        respones = admin_class.default_form_validation(self)
        if respones:
            error_list.append(respones)


        if error_list:
            raise ValidationError(error_list)
    class Meta:
        model = admin_class.model
        fields ="__all__"
    attr = {"Meta":Meta}


    _model_form_class = type("DyModelForm",(ModelForm,),attr)
    #print("model form",_model_form_class.Meta.model)
    setattr(_model_form_class,'__new__',__new__)
    setattr(_model_form_class,'clean',default_clean)
    return _model_form_class