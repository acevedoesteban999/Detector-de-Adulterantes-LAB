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
from django.urls import path,include
from django.contrib.auth.hashers import make_password 

from core.user.models import User
from django.contrib.auth.models import Group,Permission


def init():
    try:
        if not Group.objects.all().exists():
            l={
                'Developer':[
                    'is_development',
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
                    for pn in pl: 
                        p=Permission.objects.get(codename=pn)
                        g.permissions.add(p)
                except Exception as e:
                    print("E:",e)
            u=User.objects.get_or_create(
                first_name="Super User",
                username="superuser",
                is_superuser=True,
                #is_staff=True,
            )[0]
            u.set_password('superuser')
            u.save()
            u.groups.add(Group.objects.first())
    except:
        pass


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('core.process.urls')),
    path('log/',include('core.log.urls')),
    path('user/',include('core.user.urls')),
    path('conf/',include('core.conf.urls')),
    #path('process/',include('core.process.urls')),
]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
