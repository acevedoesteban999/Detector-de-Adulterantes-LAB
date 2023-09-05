from django.shortcuts import render,redirect
from django.views.generic import FormView
from .forms import NetWorkForm,DateForm
from django.contrib import messages
from core.log.utils import MyLoginRequiredMixin
# Create your views here.

class NetWorkView(MyLoginRequiredMixin,FormView):
    form_class=NetWorkForm
    template_name='conf.html'
    permission_required="is_development"
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(request,form)
        else:
            return self.form_invalid(request,form)
    
    def form_invalid(self,request,form):
        messages.error(request,'Error al actualizar fecha y hora')
        return super().form_invalid(form)
    
    def form_valid(self,request,*args, **kwargs):
        form=self.get_form()
        form.save()
        messages.success(request,'Actualizados fecha y hora correctamente')
        return redirect('process')
        
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Editar fecha y hora"
        return context
    
class DateView(MyLoginRequiredMixin,FormView):
    form_class=DateForm
    template_name='conf.html'
    permission_required="is_development"
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(request,form)
        else:
            return self.form_invalid(request,form)
    
    def form_invalid(self,request,form):
        messages.error(request,'Error al actualizar párametros de fecha y hora')
        return super().form_invalid(form)
    
    def form_valid(self,request,*args, **kwargs):
        form=self.get_form()
        form.save()
        messages.success(request,'Actualizados fecha y hora correctamente')
        return redirect('process')
        
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Editar fecha y hora"
        return context