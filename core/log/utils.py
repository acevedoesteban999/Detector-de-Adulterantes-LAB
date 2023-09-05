from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
# Create your views here.
from django.urls import reverse_lazy

class MyLoginRequiredMixin(LoginRequiredMixin,PermissionRequiredMixin):
    login_url = reverse_lazy('login')
    permission_required=None
    permission_denied_message="Permisos insuficientes para acceder a esta zona"
    
    def is_ajax(self):
        return self.request.headers.get('x-requested-with') == 'XMLHttpRequest'
    
    def has_permission(self) -> bool:
        if self.permission_required==None:
            return True

        return super().has_permission()
    