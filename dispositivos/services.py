import json

from django.conf import settings


def _cargar_json(nombre_archivo, mensaje):
    ruta = settings.BASE_DIR / "data" / nombre_archivo

    with ruta.open(encoding="utf-8") as archivo:
        datos = json.load(archivo)

    if not isinstance(datos, list):
        raise ValueError(mensaje)
    return datos


def cargar_zonas():
    return _cargar_json("zonas.json", "Se esperaba una lista de zonas")


def cargar_categorias():
    return _cargar_json("categorias.json", "Se esperaba una lista de categorias")


def cargar_dispositivos():
    return _cargar_json("dispositivos.json", "Se esperaba una lista de dispositivos")


def obtener_zona(zona_id):
    for zona in cargar_zonas():
        if zona["id"] == zona_id:
            return zona
    return None


def obtener_categoria(categoria_id):
    for categoria in cargar_categorias():
        if categoria["id"] == categoria_id:
            return categoria["nombre"]
    return "Sin categoría"


def dispositivos_por_zona(zona_id):
    return [
        dispositivo
        for dispositivo in cargar_dispositivos()
        if dispositivo["zona_id"] == zona_id
    ]


def consumo_total_zona(zona_id):
    return sum(
        dispositivo["consumo_kwh"]
        for dispositivo in dispositivos_por_zona(zona_id)
    )


def estado_zona(consumo_total, limite_kwh):
    if consumo_total > limite_kwh:
        return "ALERTA"
    return "NORMAL"


def cantidad_dispositivos(zona_id):
    return len(dispositivos_por_zona(zona_id))


def estado_zonas_resumen(consumo_total, limite_kwh):
    if consumo_total > limite_kwh:
        return "LÍMITE SUPERADO"
    return "DENTRO DEL LÍMITE"


def resumen_zonas():
    resumenes = []
    total_dispositivos = 0
    total_consumo = 0.0

    for zona in cargar_zonas():
        dispositivos = dispositivos_por_zona(zona["id"])
        cantidad = len(dispositivos)
        consumo = consumo_total_zona(zona["id"])
        total_dispositivos += cantidad
        total_consumo += consumo
        resumenes.append(
            {
                "id": zona["id"],
                "nombre": zona["nombre"],
                "cantidad_dispositivos": cantidad,
                "consumo_total": consumo,
                "limite_kwh": zona["limite_kwh"],
                "estado": estado_zonas_resumen(consumo, zona["limite_kwh"]),
            }
        )

    totales = {
        "total_zonas": len(cargar_zonas()),
        "total_dispositivos": total_dispositivos,
        "total_consumo": total_consumo,
    }
    return resumenes, totales