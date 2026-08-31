# Plan de Implementación · Fase 2 EcoEnergy · TI3041

> Evaluación Sumativa I · Fase 2 (40 pts · 40% de la nota)
> Objetivo: agregar una **tercera interfaz** "Resumen de consumo por zona" en la ruta
> `/resumen-zonas/`, integrando la arquitectura MVT ya existente, sin reemplazar el
> listado ni el detalle de la Fase 1.
>
> Este documento está escrito **para que un agente de IA pueda implementarlo** de
> forma autónoma, siguiendo el código e infraestructura ya existentes.

---

## 0. Cómo usar este plan (para el agente)

1. **No inventes** rutas, nombres ni estructuras: usa las existentes como guía.
2. **NO uses Models ni ORM.** El proyecto resuelve relaciones sobre JSON en Python
   (igual que la Fase 1). Mantén ese enfoque.
3. **NO agregues dependencias nuevas** a `requirements.txt`. Solo reutiliza las ya
   declaradas (Django y django-bootstrap5).
4. **Sigue la separación MVT:** la View prepara los datos y el contexto; el Template
   SOLO presenta valores. No pongas lógica de agregación principal en el Template.
5. **Mantén la indentación de 4 espacios** en todo el código Python.
6. Al terminar ejecuta `python manage.py check` y prueba el flujo completo.
7. Registra los commits descriptivos indicados en la sección 8 y haz `push`.

---

## 1. Objetivo y alcance

Agregar una vista general que permita **comparar rápidamente el consumo de todas las
zonas**. Es una **nueva interfaz** (no reemplaza `/zonas/` ni `/zonas/<id>/`).

- Nueva ruta: **`/resumen-zonas/`** con nombre utilizable en la etiqueta `url` de Django.
- Enlace visible en la **navegación principal** (`base.html`).
- Para **cada zona** se construye un resumen con: `id`, `nombre`, `cantidad_dispositivos`,
  `consumo_total`, `limite_kwh` y `estado`.
- La View calcula **3 totales generales**: cantidad de zonas, cantidad de dispositivos y
  consumo total de todos los dispositivos.

**Fuera de alcance:** Models, ORM, CRUD, formularios, autenticación, dependencias nuevas.

---

## 2. Estado actual del proyecto (contexto para el agente)

| Componente | Estado actual |
|---|---|
| Aplicación | `dispositivos` (instalada en `config/settings.py`) |
| Datos JSON | `data/zonas.json` (5), `data/categorias.json` (4), `data/dispositivos.json` (9) |
| `services.py` | Ya tiene: `cargar_zonas`, `cargar_categorias`, `cargar_dispositivos`, `obtener_zona`, `obtener_categoria`, `dispositivos_por_zona`, `consumo_total_zona`, `estado_zona`, `cantidad_dispositivos` |
| Vistas | `inicio`, `listar_zonas`, `detalle_zona`, `catalogo` |
| URLs | `/` (inicio), `/zonas/` (listar), `/zonas/<id>/` (detalle), `/dispositivos/` (catálogo) |
| Template base | `templates/base.html` con navbar (Inicio · Zonas · Dispositivos) |
| Bootstrap | `django-bootstrap5` (bundles CSS+JS cargados en `base.html`) |

> Nota: `estado_zona(consumo_total, limite_kwh)` en Fase 1 devuelve `"ALERTA"`/`"NORMAL"`.
> Para Fase 2 el enunciado pide **otro texto obligatorio**: `"DENTRO DEL LÍMITE"` /
> `"LÍMITE SUPERADO"`. Decide cómo hacerlo sin romper la Fase 1 (ver sección 2.1).

### 2.1 Regla de negocio Fase 2 (texto y color)

| Condición | Texto obligatorio | Bootstrap |
|---|---|---|
| `consumo_total <= limite_kwh` | `DENTRO DEL LÍMITE` | verde (`success`) |
| `consumo_total > limite_kwh` | `LÍMITE SUPERADO` | rojo (`danger`) |
| Zona sin dispositivos | cantidad `0`, consumo `0`, estado `DENTRO DEL LÍMITE` | verde |

**IMPORTANTE sobre `estado_zona`:** la función existente devuelve `NORMAL`/`ALERTA`.
La Fase 2 exige un texto DIFERENTE. Opciones recomendadas (elige una y sé consistente):

- **Opción A (recomendada):** crear una nueva función en `services.py`, p. ej.
  `estado_zona_fase2(consumo_total, limite_kwh)` que devuelva
  `"DENTRO DEL LÍMITE"` / `"LÍMITE SUPERADO"`. NO modifiques `estado_zona` para no
  romper `listar_zonas` y `detalle_zona`. La multiplicidad `<=` debe dar
  `DENTRO DEL LÍMITE` (igual que Fase 1, `<=` da NORMAL).
- **Opción B:** refactorizar `estado_zona` con un parámetro, pero esto toca la Fase 1;
  solo hazlo si verificas que `/zonas/` y `/zonas/<id>/` siguen funcionando con
  NORMAL/ALERTA.

---

## 3. Datos actuales (referencia)

`data/zonas.json` → 5 zonas (`id`, `nombre`, `limite_kwh`).

`data/dispositivos.json` → 9 dispositivos con `zona_id` y `categoria_id`.

Resumen de consumo esperado (verifícalo con el código, no lo hardcodees):

| Zona | Dispositivos | Consumo total | Límite | Estado (F2) |
|---|---|---|---|---|
| Zona 1 | (Refrigerador, Sistema solar) | sumar | 50 | calcular |
| Zona 2 | (Climatizador, Iluminación, Computador) | sumar | 30 | calcular |
| Zona 3 | (Medidor, Televisor) | sumar | 40 | calcular |
| Zona 4 | (Calefactor, Sistema de bombeo) | sumar | 50 | calcular |
| Zona 5 | (sin dispositivos) | 0 | 20 | DENTRO DEL LÍMITE |

> Zona 5 es el escenario "zona sin dispositivos" ya presente en los datos.

---

## 4. Tareas de implementación (ordenadas)

### Paso 1 · Servicio de agregación (`dispositivos/services.py`)

Agrega (o crea) una función que devuelva los resúmenes por zona y los totales generales.
Recomendación: **un solo punto de entrada** que la View consuma, p. ej.:

```python
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
        resumenes.append({
            "id": zona["id"],
            "nombre": zona["nombre"],
            "cantidad_dispositivos": cantidad,
            "consumo_total": consumo,
            "limite_kwh": zona["limite_kwh"],
            "estado": estado_zonas_resumen(consumo, zona["limite_kwh"]),
        })

    totales = {
        "total_zonas": len(cargar_zonas()),
        "total_dispositivos": total_dispositivos,
        "total_consumo": total_consumo,
    }
    return resumenes, totales
```

Implementa la función de estado acorde a tu decisión de la sección 2.1.

**Requisito en esta capa:** la lógica de conteo, suma y estado vive aquí (capa de
datos), NO en el template.

### Paso 2 · View (`dispositivos/views.py`)

Agrega una función de vista, p. ej.:

```python
def resumen_zonas(request):
    resumenes, totales = servicios.resumen_zonas()
    contexto = {
        "resumenes": resumenes,
        "totales": totales,
    }
    return render(request, "dispositivos/resumen_zonas.html", contexto)
```

- La View **carga, relaciona, agrega y construye el contexto** (separación MVT).
- No calcules los números dentro del HTML.

### Paso 3 · URL (`dispositivos/urls.py`)

Agrega la ruta con nombre:

```python
path("resumen-zonas/", views.resumen_zonas, name="resumen_zonas"),
```

- Debe ser utilizable con `{% url 'dispositivos:resumen_zonas' %}`.
- NO elimines las rutas existentes de la Fase 1.

### Paso 4 · Template (`templates/base.html` y nuevo template)

1. **`base.html`:** agrega un enlace en el `<nav>` principal, p. ej. un elemento
   `<li class="nav-item"><a class="nav-link" href="{% url 'dispositivos:resumen_zonas' %}">Resumen</a></li>`.
2. **Crear `templates/dispositivos/resumen_zonas.html`** que `{% extends "base.html" %}`
   y contenga, como mínimo (CA 4.1 del enunciado):
   - Título de la página (p. ej. `Resumen de consumo por zona`).
   - **3 tarjetas** con los totales generales:
     - Cantidad de zonas.
     - Cantidad de dispositivos.
     - Consumo total de todos los dispositivos.
   - **Tabla responsive** (`.table-responsive`) con columnas:
     `Zona | Cantidad de dispositivos | Consumo total | Límite | Estado`.
   - **Estado con texto + color** (badge de Bootstrap verde/rojo con el texto
     obligatorio). El color no puede ser el único indicador.
   - Mensaje visible si **no hay zonas** (usa `{% if %}/{% else %}` o `{% empty %}`),
     p. ej. "No existen zonas disponibles.".

Recomendación de estructura Bootstrap (coherente con `base.html`):

```
<h1> ... título ... </h1>
<div class="row row-cols-1 row-cols-md-3 g-3 mb-4">  (3 tarjetas de totales)
<div class="table-responsive"><table class="table table-striped align-middle"> ... </table></div>
```

Dentro de la tabla, por ejemplo:

```html
{% if estado == "DENTRO DEL LÍMITE" %}
  <span class="badge bg-success">&#10003; DENTRO DEL LÍMITE</span>
{% else %}
  <span class="badge bg-danger">&#9888; LÍMITE SUPERADO</span>
{% endif %}
```

> Reutiliza íconos/badges como ya hace `zona_detalle.html`.


---

## 5. Escenarios de comprobación obligatorios

Prueba la ruta `/resumen-zonas/` con los 5 escenarios del enunciado:

| Escenario | Acción de prueba | Resultado esperado |
|---|---|---|
| Nuevos registros | Agregar zonas/dispositivos válidos al JSON | Aparecen sin lógica/HTML específico por registro |
| Mayor volumen | Aumentar temporalmente zonas y dispositivos | Cálculos correctos; navegación y contenido accesibles (sin desbordes) |
| Zona sin dispositivos | Mantener una zona sin asociaciones | Fila con 0 dispositivos, consumo 0, estado `DENTRO DEL LÍMITE` |
| Colección vacía | Probar sin zonas | Página operativa y mensaje comprensible |
| Estados | Consumos bajo, igual y sobre el límite | Texto + tratamiento visual correctos según regla |

> No se evalúa recuperación ante errores de sintaxis JSON. Sí se evalúa el
> comportamiento ante cambios válidos en la cantidad de registros.

---

## 6. Criterios de aceptación → Archivo/Componente → Prueba

| Código | Criterio | Archivo/Componente | Prueba verificable |
|---|---|---|---|
| F2-1 | Ruta nombrada `/resumen-zonas/` y accesible desde navegación principal | `dispositivos/urls.py` + `templates/base.html` | Navegar desde el menú y por URL directa |
| F2-2 | Carga/relaciona JSON; calcula dinámicamente cantidades, consumos, límites, estados y totales generales, incluyendo zonas sin dispositivos | `dispositivos/services.py` + `views.resumen_zonas` | Muta JSON y recarga; sin números hardcodeados |
| F2-3 | Integración MVT correcta; la View prepara datos, aplicación sin errores | `urls` + `views` + `resumen_zonas.html` | `python manage.py check` y flujo completo |
| F2-4 | Interfaz Bootstrap con jerarquía, navegación, legibilidad, table-responsive y estados texto+color | `resumen_zonas.html` + `base.html` | Revisión visual 100% zoom; tablas con scroll, sin desbordes |
| F2-5 | Responde a add registros, mayor volumen, colecciones vacías y estados | Views/services + Templates | Ejecutar los 5 escenarios de la sección 5 |
| F2-6 | SEO de commits, push y hash entregado; código claro, 4 espacios | Git + `*.py` | `git log`, revisión de formato y push |
| F2-7 | Comprensión individual (flujo URL→View→contexto→Template) | Respuestas escritas (no código) | El estudiante explica su propio código |

> **IMPORTANTE:** la Fase 2 es **individual, SIN IA**. Este plan es solo un documento
> de apoyo/preparación. El estudiante debe implementar y explicar el código por sí
> mismo en la sesión oficial.

---

## 7. Verificación final del agente

Antes de dar por terminada la tarea:

1. `python manage.py check` → sin errores.
2. `python manage.py runserver` y abrir `/resumen-zonas/` → página correcta.
3. Verificar que `/`, `/zonas/`, `/zonas/<id>/` y `/dispositivos/` siguen funcionando
   (no se rompió la Fase 1).
4. Vaciar temporalmente `zonas.json` → mensaje de "no hay zonas".
5. Vaciar los dispositivos de una zona (p. ej. Zona 5) → fila con 0 / 0 / DENTRO DEL LÍMITE.
6. Probar un caso sobre el límite y uno bajo el límite → texto/color correctos.

