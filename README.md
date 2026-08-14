# Backend Flex EcoEnergy

API Back End del proyecto EcoEnergy, desarrollada con Python y Django.

## Descripción y objetivo

> **Descripción provisional:** este repositorio corresponde a la etapa inicial del
> Back End de EcoEnergy. Aún no se ha definido formalmente el alcance funcional del
> proyecto, por lo que el texto siguiente es un bosquejo preliminar y puede cambiar.

El objetivo de este proyecto es construir el Back End de EcoEnergy sobre Django,
entregando la base (scaffolding) sobre la cual se definirán las aplicaciones,
modelos y funcionalidades del sistema.

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
python3 -m venv .venv
```

Activación del entorno virtual:

- macOS / Linux:

  ```bash
  source .venv/bin/activate
  ```

- Windows (PowerShell):

  ```powershell
  .venv\Scripts\activate
  ```

Al activarse, el prompt de la terminal mostrará el prefijo `(.venv)`.

## Instalación desde `requirements.txt`

Con el entorno virtual activado:

```bash
pip install -r requirements.txt
```

Dependencias del proyecto:

- `Django==6.1`
- `asgiref==3.12.1`
- `sqlparse==0.6.0`

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

## Estado actual y próximos pasos

- **Estado actual:** proyecto Django recién creado con `django-admin startproject`
  (scaffolding inicial). Solo existe el proyecto `config` (settings, URLs, ASGI/WSGI),
  sin aplicaciones propias ni funcionalidad implementada.
- **Próximos pasos:** definir el alcance funcional de EcoEnergy y, a partir de él,
  crear las aplicaciones (apps) y los modelos que correspondan.

## Estructura del proyecto

```
backend-flex-EcoEnergy/
├── config/            # Proyecto Django (settings, urls, asgi, wsgi)
├── manage.py          # Utilidad de administración de Django
├── requirements.txt   # Dependencias del proyecto
└── db.sqlite3         # Base de datos local (no versionada)
```
