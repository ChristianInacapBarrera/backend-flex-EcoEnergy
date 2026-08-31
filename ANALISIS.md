# ANALISIS.md · Análisis del Sistema EcoEnergy

> Fase 1 · EcoEnergy · Evaluación Sumativa I · TI3041 · Programación Back End.
> Análisis del modelo de datos, relaciones, multiplicidades, claves de conexión
> y matriz de criterios de aceptación.

---

## 1. Modelo de datos

El sistema se construye sobre **tres entidades** almacenadas como archivos JSON
en `data/`, sin uso de Models ni ORM. Las entidades son:

```
Zona (id, nombre, limite_kwh)
Categoria (id, nombre, descripcion)
Dispositivo (id, nombre, consumo_kwh, zona_id, categoria_id)
```

### Detalle de atributos

| Entidad | Campo | Tipo | Descripción |
|---|---|---|---|
| **Zona** | `id` | int | Identificador único de la zona |
| | `nombre` | texto | Nombre de la zona (ej. "Zona 1") |
| | `limite_kwh` | float/int | Límite de consumo permitido en kWh |
| **Categoria** | `id` | int | Identificador único de la categoría |
| | `nombre` | texto | Nombre (Medición, Climatización, Iluminación, Electrodomésticos) |
| | `descripcion` | texto | Descripción de la categoría |
| **Dispositivo** | `id` | int | Identificador único del dispositivo |
| | `nombre` | texto | Nombre del dispositivo |
| | `consumo_kwh` | float | Consumo energético en kWh |
| | `zona_id` | int | FK lógica → `Zona.id` |
| | `categoria_id` | int | FK lógica → `Categoria.id` |

---

## 2. Relaciones

### Relación 1: Zona — Dispositivo

- **Tipo:** Una zona **contiene** muchos dispositivos.
- **Sentido:** `Zona (1) → (0..N) Dispositivo`.
- **Clave de conexión:** `Dispositivo.zona_id` referencia a `Zona.id`.
- Una zona puede **no** tener dispositivos (la aplicación debe seguir operativa).
- Un dispositivo **pertenece a una única zona**.

### Relación 2: Categoría — Dispositivo

- **Tipo:** Una categoría **agrupa** muchos dispositivos.
- **Sentido:** `Categoria (1) → (1..N) Dispositivo`.
- **Clave de conexión:** `Dispositivo.categoria_id` referencia a `Categoria.id`.
- No existen categorías vacías en los datos de ejemplo; cada dispositivo tiene una
  categoría asociada.

---

## 3. Multiplicidades

| Relación | Origen | Destino | Multiplicidad | Significado |
|---|---|---|---|---|
| Zona → Dispositivo | 1 Zona | 0..* Dispositivos | `1 : 0..*` | Una zona puede tener cero o muchos dispositivos |
| Categoría → Dispositivo | 1 Categoría | 1..* Dispositivos | `1 : 1..*` | Una categoría agrupa uno o más dispositivos |
| Dispositivo → Zona | 1 Dispositivo | 1 Zona | `* : 1` | Cada dispositivo pertenece a una única zona |
| Dispositivo → Categoría | 1 Dispositivo | 1 Categoría | `* : 1` | Cada dispositivo tiene una única categoría |

### Interpretación en el alcance de la Fase 1

- **`1 : 0..*` (Zona—Dispositivo):** una zona sin dispositivos está permitida y debe
  mostrarse correctamente con un mensaje claro (criterio CA-07).
- **`1 : 1..*` (Categoría—Dispositivo):** cada dispositivo referencia una categoría
  existente; si no se resuelve, se muestra el respaldo `"Sin categoría"`.

---

## 4. Claves de conexión

| Entidad | Campo clave | Tipo | Referencia |
|---|---|---|---|
| Dispositivo | `zona_id` | int | `Zona.id` |
| Dispositivo | `categoria_id` | int | `Categoria.id` |

- Son **claves foráneas lógicas** (enteras), no constraints de base de datos.
- La resolución de las relaciones se realiza en `dispositivos/services.py` mediante
  recorridos sobre las listas JSON (`obtener_zona`, `obtener_categoria`,
  `dispositivos_por_zona`).

```
Diagrama de conexiones:

  Zona.id  <──────  Dispositivo.zona_id
  Categoria.id  <──  Dispositivo.categoria_id
```

### Valores actuales de datos

| Entidad | Registros | IDs |
|---|---|---|
| Zonas | 5 | 1, 2, 3, 4, 5 |
| Categorías | 4 | 1 (Medición), 2 (Climatización), 3 (Iluminación), 4 (Electrodomésticos) |
| Dispositivos | 9 | 1..9 |

---

## 5. Lógica de negocio

- **Consumo total de una zona:** suma de `consumo_kwh` de todos los dispositivos cuya
  `zona_id` coincide; si la zona no tiene dispositivos, el consumo es `0`.
- **Estado de una zona:**
  - `ALERTA` si `consumo_total > limite_kwh`.
  - `NORMAL` en caso contrario (`consumo_total <= limite_kwh`).
- **Cantidad de dispositivos:** recuento de dispositivos asociados a la zona.
- **Categoría resuelta:** nombre de la categoría a partir de `categoria_id`, con
  respaldo `"Sin categoría"`.

La implementación se encuentra en:

| Archivo | Responsabilidad |
|---|---|
| `dispositivos/services.py` | Lectura de JSON y cálculo de métricas |
| `dispositivos/views.py` | Construcción del contexto y render |
| `templates/dispositivos/*.html` | Presentación con Bootstrap 5 |

---

## 6. Matriz de Criterios de aceptación | Archivo/Componente | Prueba

| Código | Criterio de aceptación | Archivo/Componente | Prueba |
|---|---|---|---|
| CA-01 | El listado muestra todas las zonas de `zonas.json` | `services.cargar_zonas` + `views.listar_zonas` + `templates/dispositivos/zonas.html` | Agregar una zona al JSON y verificar que aparece en `/zonas/` |
| CA-02 | Cada zona muestra nombre, límite, cantidad y acceso al detalle | `templates/dispositivos/zonas.html` (cards) + contexto de `listar_zonas` | Revisar `/zonas/` con datos válidos |
| CA-03 | El detalle muestra dispositivos, categoría, consumo, métricas y estado | `views.detalle_zona` + `templates/dispositivos/zona_detalle.html` | Revisar `/zonas/<id>/` |
| CA-04 | Cantidades, sumas y estados calculados dinámicamente | `services.estado_zona` / `consumo_total_zona` / `cantidad_dispositivos` | Sin números escritos a mano en HTML; mutar JSON y recargar |
| CA-05 | ALERTA si `consumo_total > limite_kwh`; NORMAL si `<=` | `services.estado_zona` | Usar zona con consumo mayor y menor al límite |
| CA-06 | Nuevos registros JSON se incorporan sin tocar View/Template por elemento | `services` genéricos (lista/dict) | Agregar 2 dispositivos válidos y recargar |
| CA-07 | Zona sin dispositivos operativa con mensaje claro | `{% empty %}` en `templates/dispositivos/zona_detalle.html` | Dejar una zona sin dispositivos y abrir su detalle |
| CA-08 | ID de zona inexistente → 404 controlado | `Http404` en `views.detalle_zona` + `templates/404.html` | Abrir `/zonas/999/` → página 404 de Django |
| CA-09 | Estructura estable al aumentar zonas/dispositivos | `templates/base.html` + `container` + `table-responsive` | Duplicar registros válidos y revisar navegación |
| CA-10 | Tablas extensas con scroll dentro de contenedor | `.table-responsive` en `templates/dispositivos/zona_detalle.html` y `catalogo.html` | Muchos dispositivos → scroll de tabla, no de página |
| CA-11 | Jerarquía visual coherente (header, nav, títulos, tablas, botones) | `templates/base.html` + Bootstrap 5 | Revisión visual en navegador 100% zoom |
| CA-12 | Estados con texto + apoyo visual (no solo color) | Badges + texto/íconos en templates | Zonas NORMAL y ALERTA: texto distinguible sin color |
| CA-13 | Proyecto instalable y `python manage.py check` sin errores | Repo + `requirements.txt` + `README.md` | Clonar, `pip install -r requirements.txt`, `manage.py check` |

---

## 7. Resumen

El sistema EcoEnergy maneja **3 entidades** (Zona, Categoría, Dispositivo) con
**2 relaciones** (Zona→Dispositivo `1:0..*` y Categoría→Dispositivo `1:1..*`),
conectadas mediante **2 claves de conexión** (`zona_id`, `categoria_id`) resueltas
en Python sobre archivos JSON. Todos los criterios de aceptación (CA-01 a CA-13) han
sido verificados según la matriz anterior.
