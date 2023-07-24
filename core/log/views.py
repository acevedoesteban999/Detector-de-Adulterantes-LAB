from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.views.generic import RedirectView
    
class Login(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url=reverse_lazy('process')
    
    def get_form(self, form_class=None):
        form = super(Login, self).get_form(form_class)
        for i in form.visible_fields():
            i.field.widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': f'Ingrese su {i.label.lower()}'
            })
        return form
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        login(self.request, form.get_user())
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        
    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return super().get_default_redirect_url()
        else:
            return self.success_url
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inicio de Sesión'
        return context

class Logout(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)

