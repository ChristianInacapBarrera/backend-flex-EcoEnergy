from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
"""def inicio(request): #Forma basica de mostrar contenido
    return HttpResponse(
        "<h1>EcoEnergy</h1>"
        "<p>Back End en funcionamiento</p>"
        )"""
    
#Esats funciones dirigen que mostrar

# dispositivos/views.py 
def dispositivos_zona(request, zona_id): #clase 3
    if zona_id != 3:
        return HttpResponse(
            "Zona no encontrada", status=404
        )
    return HttpResponse( 
        f"Dispositivos de la zona {zona_id}"
    )
    
def dispositivos_id(request, dispositivo_id): #implementacion autonoma
    if dispositivo_id == 10:
        context2 = {"mensaje": f"Dispositivo {dispositivo_id} inexistente"}
    else:
        context2= {"mensaje": f"Dispositivo {dispositivo_id} encontrado."}
    
    
    return render(
        request,
        "dispositivos/dispositivo.html",
        context2,
    )
    
def inicio(request):
    contexto = {
        "sistema": "EcoEnergy",
        "mensaje": "Monitoreo energico responsable",
        "asignatura": "Programación Back End",
    }
    return render(
        request,
        "dispositivos/inicio.html",
        contexto,
    )
    
def catalogo(request):
    dispositivos = [
        {"nombre":"Medidor inteligente", "estado": "Activo"},
        {"nombre":"Sensor de temperatura", "estado": "Activo"},
        {"nombre":"Climatizador", "estado": "Revisión"}
    ]
    return render(
        request,
        "dispositivos/catalogo.html",
        {"dispositivos": dispositivos},
    )