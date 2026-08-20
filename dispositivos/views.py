from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
def inicio(request):
    return HttpResponse(
        "<h1>EcoEnergy</h1>"
        "<p>Back End en funcionamiento</p>"
        )
    
# dispositivos/views.py 
def dispositivos_zona(request, zona_id): 
    if zona_id != 3:
        return HttpResponse(
            "Zona no encontrada", status=404
        )
    return HttpResponse( 
        f"Dispositivos de la zona {zona_id}"
    )
    
def dispositivos_id(request, dispositivo_id):
    if dispositivo_id != 10:
        return HttpResponse(
            "Dispositivo inexistente", status=404
        )
    return HttpResponse(
        f"Dispositivo {dispositivo_id} encontrado."
    )