from django.shortcuts import render,HttpResponse

# Create your views here.
from django.shortcuts import render


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from core.chann.consumers import send_message
 
def asd(request):
    send_message("Hola Mundo")
    return HttpResponse("OK")

def room(request):
    return render(request, "room.html")
