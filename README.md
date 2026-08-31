# Backend Flex EcoEnergy

API Back End del proyecto **EcoEnergy**, desarrollada con Python y Django. Sistema de monitoreo energético que permite visualizar zonas de consumo, dispositivos asociados, categorías y estados de alerta.

## Descripción y objetivo

EcoEnergy es una aplicación web backend construida sobre Django que gestiona el monitoreo de consumo energético. El sistema carga datos de zonas, categorías y dispositivos desde archivos JSON y permite:

- Listar todas las zonas de consumo con sus métricas.
- Consultar el detalle de cada zona: dispositivos, categoría, consumo total y estado (NORMAL/ALERTA).
- Visualizar un catálogo completo de dispositivos.
- Manejar errores con página 404 controlada para IDs inexistentes.

**Enfoque:** La aplicación utiliza archivos JSON como única fuente de datos (sin Models ni ORM), resolviendo relaciones entre entidades mediante estructuras Python.

## Requisitos previos

- Python 3.12 o superior (Django 6.1 requiere Python 3.12+).
- `pip` (incluido con Python).
- `git`.
- Un entorno macOS/Linux o Windows con acceso a terminal.

## Clonación del repositorio

```bash
git clone https://github.com/ChristianInacapBarrera/backend-flex-EcoEnergy.git
cd backend-flex-EcoEnergy
```

## Creación y activación de `.venv`

Desde la raíz del proyecto:

```bash
python3 -m venv venv
```

Activación del entorno virtual:

- macOS / Linux:

  ```bash
  source venv/bin/activate
  ```

- Windows (PowerShell):

  ```powershell
  venv\Scripts\activate
  ```

Al activarse, el prompt de la terminal mostrará el prefijo `(venv)`.

## Instalación desde `requirements.txt`

Con el entorno virtual activado:

```bash
pip install -r requirements.txt
```

Dependencias del proyecto:

| Paquete | Versión | Propósito |
|---|---|---|
| `Django` | 6.1 | Framework web |
| `django-bootstrap5` | 26.2 | Integración Bootstrap 5 en templates |
| `asgiref` | 3.12.1 | Referencias ASGI (dependencia de Django) |
| `sqlparse` | 0.6.0 | Parsing SQL (dependencia de Django) |

## Comandos de verificación

Con el entorno virtual activado y desde la raíz del proyecto:

```bash
python manage.py check
```

Para ejecutar el servidor de desarrollo:

```bash
python manage.py runserver
```

El servidor se levanta en `http://127.0.0.1:8000/`.

## Rutas funcionales

| Ruta | Método | Descripción |
|---|---|---|
| `/` | GET | Página de inicio del sistema |
| `/zonas/` | GET | Listado de todas las zonas con métricas de consumo |
| `/zonas/<id>/` | GET | Detalle de una zona específica con sus dispositivos |
| `/dispositivos/` | GET | Catálogo completo de dispositivos |
| `/admin/` | GET | Panel de administración Django |

## Estructura del proyecto

```
backend-flex-EcoEnergy/
├── config/                    # Configuración Django (settings, urls, asgi, wsgi)
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── dispositivos/              # Aplicación principal
│   ├── models.py              # (sin uso - datos en JSON)
│   ├── views.py               # Vistas: inicio, listar_zonas, detalle_zona, catalogo
│   ├── urls.py                # Rutas de la aplicación
│   ├── services.py            # Capa de servicios: carga y transformación de datos JSON
│   ├── admin.py               # Registro admin (pendiente)
│   ├── tests.py               # Pruebas automatizadas
│   └── migrations/
├── data/                      # Fuentes de datos JSON
│   ├── zonas.json             # 5 zonas de consumo
│   ├── categorias.json        # 4 categorías de dispositivos
│   └── dispositivos.json      # 9 dispositivos energéticos
├── templates/                 # Templates HTML (Bootstrap 5)
│   ├── base.html              # Plantilla base con navbar
│   ├── 404.html               # Página de error 404
│   └── dispositivos/
│       ├── inicio.html        # Página de inicio
│       ├── zonas.html         # Listado de zonas (cards)
│       ├── zona_detalle.html  # Detalle de zona (métricas + tabla)
│       └── catalogo.html      # Catálogo de dispositivos
├── venv/                      # Entorno virtual (no versionado)
├── db.sqlite3                 # Base de datos SQLite (no usada)
├── manage.py                  # Utilidad de administración Django
├── requirements.txt           # Dependencias del proyecto
├── PLAN_IMPLEMENTACION.md     # Plan de implementación Fase 1
├── IA.md                      # Documentación de uso de IA
├── ANALISIS.md                # Análisis del sistema y criterios de aceptación
└── .gitignore
```

## Datos de ejemplo

### Zonas (`data/zonas.json`)
5 zonas con límites de consumo en kWh.

### Categorías (`data/categorias.json`)
Medición, Climatización, Iluminación y Electrodomésticos.

### Dispositivos (`data/dispositivos.json`)
9 dispositivos distribuidos en las zonas, con consumo individual en kWh y referencia a zona y categoría.

## Escenarios de prueba

| Escenario | Acción | Resultado esperado |
|---|---|---|
| Nuevos registros | Agregar dispositivos válidos al JSON | Aparecen; cantidades y consumo se actualizan |
| Mayor volumen | Duplicar registros válidos | Estructura y navegación se conservan |
| Colección vacía | Zona sin dispositivos | Mensaje claro; app sigue funcionando |
| ID inexistente | Abrir `/zonas/999/` | 404 controlado sin falla técnica |
| Estados | Datos que producen NORMAL y ALERTA | Texto y señal visual correctos |

## Documentación adicional

- **[PLAN_IMPLEMENTACION.md](PLAN_IMPLEMENTACION.md)** - Plan detallado de implementación de la Fase 1.
- **[ANALISIS.md](ANALISIS.md)** - Análisis de relaciones, multiplicidades y matriz de criterios de aceptación.
- **[IA.md](IA.md)** - Documentación de herramientas y prompts de IA utilizados.
