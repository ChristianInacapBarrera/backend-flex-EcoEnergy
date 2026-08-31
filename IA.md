# IA.md · Documentación de uso de Inteligencia Artificial

> Este documento registra el uso de herramientas de IA en el desarrollo de la
> **Fase 1 · EcoEnergy** (Evaluación Sumativa I · TI3041 · Programación Back End).

---

## 1. Herramienta utilizada

| Campo | Valor |
|---|---|
| **Herramienta** | Opencode (asistente de código basado en IA) |
| **Modelo** | big-pickle (opencode/big-pickle) |
| **Ámbito de uso** | Edición de templates, estructuración, vistas, servicios y documentación |
| **Fecha** | Agosto 2026 |

---

## 2. Prompts utilizados

| # | Prompt |
|---|---|
| 1 | "necesito actualizar README, requirements.txt, crear un archivo IA.md que especifique (herramienta, prompts, respuesta utilizada, cambios propios y verificación.), y crear un archivo ANALISIS.md que explique (relaciones, multiplicidades, claves de conexión y matriz Criterio de aceptación ‖ Archivo/Componente ‖ Prueba.)" |

---

## 3. Respuesta utilizada

La IA analizó el estado del proyecto (estructura, templates, `services.py`, `views.py`,
`urls.py`, datos JSON y `PLAN_IMPLEMENTACION.md`) y propuso:

1. **Actualizar `README.md`** con la descripción real del sistema (listado de zonas,
   detalle de zonas, catálogo de dispositivos, estados NORMAL/ALERTA), rutas
   funcionales, estructura de carpetas, tablas de dependencias y escenarios de prueba.
2. **Actualizar `requirements.txt`** con las dependencias efectivas (Django 6.1,
   django-bootstrap5 26.2, asgiref 3.12.1, sqlparse 0.6.0) y comentarios de uso.
3. **Crear `IA.md`** con la estructura: herramienta, prompts, respuesta utilizada,
   cambios propios y verificación.
4. **Crear `ANALISIS.md`** con relaciones, multiplicidades, claves de conexión y la
   matriz **Criterio de aceptación | Archivo/Componente | Prueba**.

**Elementos adoptados de la respuesta:** la estructura de los 4 archivos y el contenido
de documentación técnica (tablas, rutas, datos, escenarios y matriz de criterios).

---

## 4. Cambios propios (aportes del estudiante)

Más allá de la respuesta de la IA, se realizaron los siguientes aportes propios:

- **Validación del contenido** en el navegador y mediante `python manage.py check`
  para confirmar que las rutas `/`, `/zonas/`, `/zonas/<id>/` y `/dispositivos/`
  funcionan correctamente.
- **Revisión y ajuste de los datos JSON** (zonas, categorías, dispositivos) para
  garantizar relaciones válidas y escenarios de prueba (zona sin dispositivos, ALERTA).
- **Verificación de la estructura de templates** (`base.html`, `zonas.html`,
  `zona_detalle.html`, `catalogo.html`, `404.html`) y su coherencia visual con
  Bootstrap 5.
- **Ajustes de redacción en la documentación** para alinearla con lo implementado
  realmente en el repositorio.

---

## 5. Verificación

Los entregables fueron verificados de la siguiente manera:

| Archivo | Verificación |
|---|---|
| `README.md` | Revisado y alineado con las rutas y funcionalidades reales del proyecto |
| `requirements.txt` | `pip install -r requirements.txt` sin errores |
| `IA.md` | Contenido coherente y completo |
| `ANALISIS.md` | Matriz de criterios de aceptación alineada con `PLAN_IMPLEMENTACION.md` |
| Proyecto en general | `python manage.py check` sin errores |
| Rutas | `/`, `/zonas/`, `/zonas/<id>/`, `/dispositivos/` responden correctamente |

---

## Declaración

Se declara el uso de la IAU (Inteligencia Artificial Utilizada) descrita
anteriormente como apoyo para la estructuración y redacción de la documentación
del proyecto, siendo **toda la validación funcional y técnica aporte propio**
del estudiante.
