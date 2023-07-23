from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.urls import reverse_lazy

class MyLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')
