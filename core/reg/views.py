from django.views.generic import TemplateView
from core.log.utils import MyLoginRequiredMixin
from core.pred.models import Prediction
from core.tra.models import Training,Model
# Create your views here.
class RegistersView(MyLoginRequiredMixin,TemplateView):
    template_name="registers.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count_pred"] = Prediction.objects.count()
        context["count_tra"] = Training.objects.count() 
        context["count_mod"] = Model.objects.count() 
        return context
    
