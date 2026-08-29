from django.shortcuts import render

from .services import (
    cantidad_dispositivos,
    cargar_dispositivos,
    cargar_zonas,
    consumo_total_zona,
    estado_zona,
    obtener_categoria,
    obtener_zona,
)


def inicio(request):
    contexto = {
        "sistema": "EcoEnergy",
        "mensaje": "Monitoreo energético responsable",
        "asignatura": "Programación Back End",
    }
    return render(request, "dispositivos/inicio.html", contexto)


def listar_zonas(request):
    zonas = []
    for zona in cargar_zonas():
        zona_id = zona["id"]
        zonas.append(
            {
                "id": zona_id,
                "nombre": zona["nombre"],
                "limite_kwh": zona["limite_kwh"],
                "cantidad_dispositivos": cantidad_dispositivos(zona_id),
                "consumo_total": consumo_total_zona(zona_id),
                "estado": estado_zona(
                    consumo_total_zona(zona_id), zona["limite_kwh"]
                ),
            }
        )
    return render(request, "dispositivos/zonas.html", {"zonas": zonas})


def detalle_zona(request, zona_id):
    zona = obtener_zona(zona_id)
    if zona is None:
        return render(request, "404.html", status=404)

    dispositivos = []
    for dispositivo in cargar_dispositivos():
        if dispositivo["zona_id"] == zona_id:
            dispositivos.append(
                {
                    "nombre": dispositivo["nombre"],
                    "consumo_kwh": dispositivo["consumo_kwh"],
                    "categoria": obtener_categoria(dispositivo["categoria_id"]),
                }
            )

    consumo_total = consumo_total_zona(zona_id)
    contexto = {
        "zona": zona,
        "dispositivos": dispositivos,
        "consumo_total": consumo_total,
        "cantidad_dispositivos": len(dispositivos),
        "estado": estado_zona(consumo_total, zona["limite_kwh"]),
    }
    return render(request, "dispositivos/zona_detalle.html", contexto)


def catalogo(request):
    dispositivos = []
    for dispositivo in cargar_dispositivos():
        dispositivos.append(
            {
                "nombre": dispositivo["nombre"],
                "consumo_kwh": dispositivo["consumo_kwh"],
                "categoria": obtener_categoria(dispositivo["categoria_id"]),
            }
        )
    contexto = {
        "dispositivos": dispositivos,
        "total": len(dispositivos),
    }
    return render(request, "dispositivos/catalogo.html", contexto)