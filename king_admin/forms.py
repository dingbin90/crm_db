from django.forms import forms,ModelForm


def create_model_form(request,admin_class):
    '''动态生成MODEL FORM'''
    def __new__(cls,*args,**kwargs):
        for field_name,field_obj in cls.base_fields.items():

            field_obj.widget.attrs['class']='form-control'
        return ModelForm.__new__(cls)
    class Meta:
        model = admin_class.model
        fields ="__all__"
    attr = {"Meta":Meta}


    _model_form_class = type("DyModelForm",(ModelForm,),attr)
    print("model form",_model_form_class.Meta.model)
    setattr(_model_form_class,'__new__',__new__)
    return _model_form_class