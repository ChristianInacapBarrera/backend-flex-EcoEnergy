# Plan de Implementación · Fase 1 EcoEnergy · TI3041

> Evaluación Sumativa I · Fase 1 (60 pts · 60% de la nota)
> Objetivo: listar zonas y consultar su detalle usando Django + Templates Bootstrap,
> con los 3 JSON como única fuente de datos (sin Models ni ORM).

---

## 1. Objetivo y alcance

Construir la aplicación Django que permita:

- Listar todas las zonas de `zonas.json` (**`/zonas/`**).
- Consultar el detalle de una zona (**`/zonas/<id>/`**): dispositivos, categoría,
  consumo total y estado (NORMAL/ALERTA) respecto del límite.
- Resolver relaciones entre los 3 JSON con estructuras Python (no SQL).
- Seguir funcionando ante: nuevos registros válidos, mayor volumen, zonas sin
  dispositivos e identificadores inexistentes (404 controlado).

**Fuera de alcance** (no aportan puntaje): Models, migraciones, ORM, CRUD,
formularios, autenticación, permisos, soft delete, múltiples organizaciones.

---

## 2. Estado actual del proyecto (análisis de brechas)

| Componente | Estado hoy | Brecha para la Fase 1 |
|---|---|---|
| Proyecto `config` y app `dispositivos` | Listo | — |
| `requirements.txt` | Django 6.1, django-bootstrap5, asgiref, sqlparse | OK; justificar django-bootstrap5 en ANALISIS.md (criterio F1-3) |
| `.gitignore` | Excluye `venv/`, `.env/`, `db.sqlite3` | OK |
| `data/zonas.json` | 4 registros (`id`, `nombre`, `limite_kwh`) | OK (mínimo 3) |
| `data/categorias.json` | 4 registros (`id`, `nombre`, `descripcion`) | OK (mínimo 3) |
| `data/dispositivos.json` | 8 registros (`id`, `nombre`, `consumo_kwh`, `zona_id`, `categoria_id`) | OK (mínimo 8) |
| `dispositivos/services.py` | Solo `cargar_dispositivos()` | Falta cargar zonas/categorías y lógica de relación, suma y estado |
| `dispositivos/views.py` | Views legacy y hardcodeadas (`dispositivos_zona` con `if zona_id != 3`, `dispositivos_id`, `catalogo` duplicado) | Reemplazar por vistas reales de listado/detalle de zonas |
| `dispositivos/urls.py` | Rutas legacy (`/zonas/<id>/dispositivos/`, `/dispositivos/<id>/`) | Definir `/zonas/` y `/zonas/<id>/` |
| `templates/` | `base.html`, `inicio.html`, `catalogo.html`, `dispositivo.html` | Crear templates de zonas y detalle; refinar jerarquía Bootstrap y accesibilidad |
| `templates/dispositivos/catalogo.html` | Muestra clave `estado` inexistente en JSON | Corregir (o eliminar vista si no se usa) |
| Docs (`ANALISIS.md`, `IA.md`, `README.md`) | README provisional | Crear/actualizar los 3 |
| Tests (`dispositivos/tests.py`) | Vacío | Añadir pruebas de los escenarios de la evaluación (valor añadido) |
| Git | 8 commits existentes | Al menos 4 progresivos finales + commit **"Entrega fase 1 evaluacion unidad 1"** |

---

## 3. Modelo de datos y relaciones (para ANALISIS.md)

Derivado de la Figura 1 (UML) del enunciado y de las claves exigidas en cada JSON:

```
Zona (id, nombre, limite_kwh)
  └─ Tiene 0..N dispositivos  (clave de conexión: dispositivos.zona_id -> zonas.id)

Categoria (id, nombre, descripcion)
  └─ Agrupa 1..N dispositivos (clave de conexión: dispositivos.categoria_id -> categorias.id)

Dispositivo (id, nombre, consumo_kwh, zona_id, categoria_id)
```

- **Multiplicidad Zona—Dispositivo:** `1 : 0..*` (CA-07 exige zona sin dispositivos operativa).
- **Multiplicidad Categoria—Dispositivo:** `1 : 1..*`.
- **Claves de conexión:** `zona_id` y `categoria_id` son FK lógicas (enteras) sobre
  `zonas.id` y `categorias.id`.
- **Tipos:** `id`, `zona_id`, `categoria_id`, `limite_kwh` → números (int/float);
  `consumo_kwh` → número decimal; `nombre`/`descripcion` → texto.

---

## 4. Arquitectura MVT (sin Models)

```
URL                        View (Python)                    Template (Bootstrap)
-----------------------------------------                   --------------------
/                             inicio()                        inicio.html
/zonas/                       listar_zonas()                  zonas.html
/zonas/<int:zona_id>/         detalle_zona(zona_id)           zona_detalle.html
```

- **`services.py`** concentra la lectura y transformación de datos (capa de datos).
- **`views.py`** usa `services` para construir el contexto; nunca mete JSON "a mano" en el template.
- **`base.html`** define header/nav y jerarquía; todas las vistas heredan de él (CA-11).

---

## 5. Tareas de implementación (ordenadas)

### Paso 1 · Servicios de datos (`dispositivos/services.py`)
Reemplazar el contenido actual por funciones reutilizables y robustas:

1. `cargar_zonas()` → lista de dicts de `zonas.json`.
2. `cargar_categorias()` → lista de dicts de `categorias.json`.
3. `cargar_dispositivos()` → lista de dicts de `dispositivos.json` (conservar la validación de lista).
4. `obtener_zona(zona_id)` → dict de la zona (o `None` si no existe) — evita excepción en 404.
5. `obtener_categoria(categoria_id)` → nombre o `"Sin categoría"` como respaldo.
6. `dispositivos_por_zona(zona_id)` → lista filtrada.
7. `consumo_total_zona(zona_id)` → `sum()` de `consumo_kwh` de la zona (0 si no hay dispositivos).
8. `estado_zona(consumo_total, limite_kwh)` → `"ALERTA"` si `consumo_total > limite_kwh`, si no `"NORMAL"` (CA-05).
9. `cantidad_dispositivos(zona_id)` → `len()` de los de la zona.

Toda métrica se calcula en Python, nunca se escribe manualmente en el template (CA-04, CA-06).

### Paso 2 · Views (`dispositivos/views.py`)
Limpiar el código legacy y dejar solo:

1. `inicio(request)` (conservar, ajustar contexto).
2. `listar_zonas(request)`:
   - Para cada zona agrega `cantidad_dispositivos`, `consumo_total` y `estado`.
   - Render `zonas.html`; si no hay zonas, mostrar "No hay zonas disponibles" (CA-07/`empty`).
3. `detalle_zona(request, zona_id)`:
   - `zona = obtener_zona(zona_id)`; si `None` → `raise Http404("La zona solicitada no existe")` (CA-08).
   - Contexto: zona, dispositivos (con `categoria` resuelta), `consumo_total`, `estado`.
   - Render `zona_detalle.html`.
4. (Opcional) Simplificar `catalogo` de dispositivos con claves reales del JSON o eliminar la vista/ruta.

### Paso 3 · URLS (`dispositivos/urls.py` y `config/urls.py`)
```python
path("", views.inicio, name="inicio"),
path("zonas/", views.listar_zonas, name="zonas"),
path("zonas/<int:zona_id>/", views.detalle_zona, name="detalle_zona"),
```
- Eliminar rutas legacy (`/zonas/<id>/dispositivos/`, `/dispositivos/<id>/`).
- `config/urls.py` ya incluye `dispositivos.urls` bajo `""` (se conserva; `admin/` puede quedar).

### Paso 4 · Templates Bootstrap
- **`base.html`**: header "ECoEnergy" + navbar con **Inicio · Zonas** (Bootstrap 5).
  Contenedor `container`, jerarquía visual coherente, `{% block content %}` (CA-11).
- **`zonas.html`**: tarjetas (`card`) por zona con nombre, "Límite: X kWh",
  "Dispositivos: N" y botón **Ver detalle** → `detalle_zona`. Estados con
  badge/ícono + texto (no solo color) (CA-12). `{% empty %}` → "No hay zonas disponibles".
- **`zona_detalle.html`**: título "Detalle de zona: <nombre>", tarjetas de métricas
  (Límite, Consumo total, Dispositivos, Estado con `badge-success`/`badge-danger` + texto e ícono).
  Tabla de dispositivos dentro de `.table-responsive` (scroll horizontal si es extensa, CA-10);
  columnas **Dispositivo · Categoría · Consumo kWh**. `{% empty %}` → "Esta zona no tiene dispositivos" (CA-07).

### Paso 5 · Pruebas automatizadas (`dispositivos/tests.py`) [valor añadido]
Cubrir escenarios de la Sección 6 del enunciado:
1. Nuevos registros válidos → aparecen y actualizan cantidades/suma/estado.
2. Mayor volumen → listado y detalle conservan estructura (verificar conteos).
3. Zona sin dispositivos → mensaje claro y 200.
4. `/zonas/999/` → 404 controlado.
5. Datos que producen NORMAL y ALERTA → textos correctos.

### Paso 6 · Documentación y entregables
1. **`ANALISIS.md`** — secciones:
   - Relaciones y multiplicidades (Sección 3 de este plan).
   - Claves de conexión.
   - Matriz **Criterio de aceptación | Archivo/Componente | Prueba** (tabla CA-01..CA-13).
2. **`IA.md`** — herramientas/prompts usados, respuesta utilizada, cambios propios y
   verificación; o declarar "No se utilizó IA".
3. **`README.md`** — actualizar: requisitos, instalación, ejecución, rutas funcionales
   y cómo probar cada escenario.
4. Revisar `requirements.txt` y `.gitignore` (ya correctos).

### Paso 7 · Git y entrega
1. Cumplir al menos 4 commits **progresivos y comprensibles** (evitar mensajes genéricos),
   por ejemplo:
   - "Carga y relación de zonas, categorías y dispositivos desde JSON"
   - "Views y URLs de listado y detalle de zonas con 404"
   - "Templates Bootstrap de listado y detalle de zonas"
   - "Agrega ANALISIS.md, IA.md y actualiza README"
   - "Agrega pruebas automatizadas de escenarios Fase 1"
2. Commits de prueba final, ejecutar `python manage.py check`.
3. Commit final con mensaje exacto: **`Entrega fase 1 evaluacion unidad 1`**.
4. `git push origin main` y publicar en el AMBIENTE DE APRENDIZAJE la **URL del repositorio
   y el hash exacto** de ese commit.

---

## 6. Criterios de aceptación → Archivo/Componente → Prueba

| Código | Criterio | Archivo/Componente | Prueba verificable |
|---|---|---|---|
| CA-01 | El listado muestra todas las zonas de zonas.json | `services.cargar_zonas` + `views.listar_zonas` + `zonas.html` | Agregar una zona al JSON y verificar que aparece en `/zonas/` |
| CA-02 | Cada zona muestra nombre, límite, cantidad y acceso al detalle | `zonas.html` (cards) + contexto | Revisar `/zonas/` con datos válidos |
| CA-03 | El detalle muestra dispositivos, categoría, consumo, métricas y estado | `detalle_zona` + `zona_detalle.html` | Revisar `/zonas/<id>/` |
| CA-04 | Cantidades, sumas y estados calculados dinámicamente | `services.estado_zona` / `consumo_total_zona` | Sin números escritos a mano en HTML; mutar JSON y recargar |
| CA-05 | ALERTA si `consumo_total > limite_kwh`; NORMAL si `<=` | `services.estado_zona` | Usar zona con consumo mayor y menor al límite |
| CA-06 | Nuevos registros JSON se incorporan sin tocar View/Template por elemento | `services` genéricos (lista/dict) | Agregar 2 dispositivos válidos y recargar |
| CA-07 | Zona sin dispositivos operativa con mensaje claro | `{% empty %}` en `zona_detalle.html` | Dejar una zona sin dispositivos y abrir su detalle |
| CA-08 | ID de zona inexistente → 404 controlado | `Http404` en `detalle_zona` | Abrir `/zonas/999/` → página 404 de Django |
| CA-09 | Estructura estable al aumentar zonas/dispositivos | `base.html` + `container` + `table-responsive` | Duplicar registros válidos y revisar navegación |
| CA-10 | Tablas extensas con scroll dentro de contenedor | `.table-responsive` en `zona_detalle.html` | Muchos dispositivos → scroll de tabla, no de página |
| CA-11 | Jerarquía visual coherente (header, nav, títulos, tablas, botones) | `base.html` + Bootstrap 5 | Revisión visual en navegador 100% zoom |
| CA-12 | Estados con texto + apoyo visual (no color solo) | Badges + texto/íconos en templates | Zonas NORMAL y ALERTA: texto distinguible sin color |
| CA-13 | Proyecto instalable y `python manage.py check` sin errores | Repo + `requirements.txt` + README | Clonar, `pip install -r requirements.txt`, `manage.py check` |

---

## 7. Escenarios de comprobación (Sección 6 del enunciado)

| Escenario | Acción | Resultado esperado |
|---|---|---|
| 1. Nuevos registros | Agregar 2 dispositivos válidos al JSON | Aparecen; cantidades, consumo y estado se actualizan |
| 2. Mayor volumen | Duplicar temporalmente registros válidos | Estructura, navegación y acceso se conservan |
| 3. Colección vacía | Zona sin dispositivos | Mensaje claro; app sigue funcionando |
| 4. ID inexistente | `/zonas/<inexistente>/` | 404 controlado (Django), sin falla técnica expuesta |
| 5. Estados | Datos que producen NORMAL y ALERTA | Texto y señal visual correctos |

> Nota: no se recuperan errores de sintaxis JSON (fuera de alcance).

---

## 8. Entregables obligatorios (checklist final)

- [ ] Repositorio individual accesible (URL + hash en AMBIENTE DE APRENDIZAJE).
- [ ] Código Django + 3 JSON (`zonas`, `categorias`, `dispositivos`).
- [ ] `ANALISIS.md` (relaciones, multiplicidades, claves, matriz CA | Archivo | Prueba).
- [ ] `IA.md` (herramientas/prompts o declaración de no uso de IA).
- [ ] `README.md` (requisitos, instalación, ejecución, rutas, pruebas).
- [ ] `requirements.txt` y `.gitignore` actualizados.
- [ ] Al menos 4 commits progresivos y comprensibles.
- [ ] Hash del commit **"Entrega fase 1 evaluacion unidad 1"** publicado.
- [ ] `python manage.py check` sin errores.
- [ ] Sin `venv/`, credenciales ni archivos personales en el repo.