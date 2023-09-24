"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,reverse_lazy
from django.shortcuts import render,HttpResponse
from django.views.generic import TemplateView
from core.log.utils import MyLoginRequiredMixin
from core.user.models import User
from django.contrib.auth.models import Group,Permission
from django.views.generic import RedirectView

def init_groups_permission_sueruser(init=False):
    context=""
    try:
        bool=True
        
        bool= not (init==True and Group.objects.all().exists()) 
        
        if bool==True:
            l={
                'Developer':[
                    'is_development',
                    'view_user',
                    'add_user',
                    'change_user',
                    'delete_user',
                    'act_desact_user',
                    'view_performance',
                    'view_binnacle',
                ],
                'Admin':[
                    'is_admin',
                ],
                'Guest':[
                    'is_guest',
                ]
            }
            for gn,pl in l.items():
                try:
                    g=Group.objects.get_or_create(name=gn)[0]
                    print(gn)
                    context+="{}<br>".format(gn)
                    for pn in pl: 
                        try:
                            p=Permission.objects.get(codename=pn)
                            print("\t",pn)
                            context+="<dd>{}</dd><br>".format(pn)
                            g.permissions.add(p)
                        except Exception as e:
                            print("E!:",e,":",pn)
                            context+="<br>Error:{}:    {}<br><br>".format(e,pn)
                except Exception as e:
                    print("E!:",e,":",gn)
                    context+="<br>Error:{}:    {}<br><br>".format(e,gn)
            u=User.objects.get_or_create(
                first_name="Super User",
                username="superuser",
                is_superuser=True,
                is_staff=True,
            )
            uu=u[1]
            u=u[0]
            if uu==True:
                u.set_password('superuser')
                u.save()
            u.groups.add(Group.objects.get(name="Developer"))
            print('superuser')
            context+="{} Super User<br>".format("Created" if uu==True else "See",gn)
            context+="<br><a href='{}' role='btn'>Volver</a>".format(reverse_lazy('process'))
    except:
        pass
    return context
    
init_groups_permission_sueruser(True)


class InitView(MyLoginRequiredMixin,TemplateView):
    def get(self,request):
        if request.user.is_superuser:
            return HttpResponse(init_groups_permission_sueruser())
        return render(request,'403.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('init/',InitView.as_view()),
    #path('',include('core.process.urls')),
    path('log/',include('core.log.urls')),
    path('user/',include('core.user.urls')),
    path('conf/',include('core.conf.urls')),
    path('perf/',include('core.perf.urls')),
    path('binn/',include('core.binn.urls')),
    path('pro/tra/',include('core.tra.urls')),
    path('pro/meas/',include('core.meas.urls')),
    path('pro/reg/',include('core.reg.urls')),
    path('pro/mod/',include('core.mod.urls')),
    path('',RedirectView.as_view(url='pro/reg/')),
]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
