# ioseluiz blog

Blog personal sobre Desarrollo de Software e Ingeniería Estructural, construido con Django y Python.

## Stack

| Capa | Tecnología |
|------|-----------|
| Backend | Django 4.2, Python 3.12 |
| Base de datos | PostgreSQL 15 |
| Contenedores | Docker + Docker Compose |
| Frontend | Tailwind CSS v4 Standalone |
| Markdown | Python-Markdown + pymdownx + Pygments |
| Fórmulas matemáticas | MathJax v3 |
| Editor admin | EasyMDE (dark theme) |

## Funcionalidades

- **Posts** en Markdown con soporte de fórmulas matemáticas (`$...$`, `$$...$$`), snippets de código con syntax highlighting e imágenes incrustadas
- **Dos categorías**: Desarrollo de Software e Ingeniería Estructural
- **Buscador** de posts por título y contenido
- **Registro y autenticación** de usuarios
- **Comentarios** moderados por el administrador (solo usuarios registrados)
- **Admin** con editor Markdown interactivo (EasyMDE) y subida de imágenes

## Requisitos

- Docker y Docker Compose
- Python 3.12+ (solo si se corre sin Docker)

## Inicio rápido

```bash
# 1. Clonar el repositorio
git clone git@github.com:ioseluiz/ioseluiz_blog.git
cd ioseluiz_blog

# 2. Crear el archivo de entorno
cp .env.example .env
# Editar .env con los valores reales

# 3. Levantar los contenedores
docker-compose up --build

# 4. En otra terminal, aplicar migraciones
docker-compose run --rm web python manage.py migrate

# 5. Crear superusuario
docker-compose run --rm web python manage.py createsuperuser
```

La aplicación queda disponible en `http://localhost:8000` y el panel de administración en `http://localhost:8000/admin/`.

## Variables de entorno

Copiar `.env.example` a `.env` y completar los valores:

```env
SECRET_KEY=           # Clave secreta de Django
DEBUG=True            # False en producción
ALLOWED_HOSTS=        # Hosts permitidos (separados por coma)

DB_NAME=              # Nombre de la base de datos
DB_USER=              # Usuario de PostgreSQL
DB_PASSWORD=          # Contraseña de PostgreSQL
DB_HOST=db            # Host (db para Docker, localhost si corre local)
DB_PORT=5432

POSTGRES_DB=          # Igual que DB_NAME
POSTGRES_USER=        # Igual que DB_USER
POSTGRES_PASSWORD=    # Igual que DB_PASSWORD
```

## Settings

| Módulo | Uso |
|--------|-----|
| `settings/base.py` | Configuración común |
| `settings/local.py` | Desarrollo local (DEBUG=True, debug toolbar) |
| `settings/production.py` | Producción (HTTPS, whitenoise, seguridad) |

La variable `DJANGO_SETTINGS_MODULE` en `.env` controla cuál se usa.

## Comandos útiles (Makefile)

```bash
make up              # Levantar contenedores
make down            # Detener contenedores
make migrate         # Aplicar migraciones
make makemigrations  # Crear migraciones
make createsuperuser # Crear administrador
make shell           # Shell de Django
make logs            # Ver logs del servidor
make tailwind-build  # Compilar CSS de producción
```

## Estructura del proyecto

```
blog_ioseluiz/
├── apps/
│   ├── accounts/     # CustomUser, registro, login, logout
│   ├── posts/        # Modelo Post, vistas, templatetags de Markdown
│   └── comments/     # Modelo Comment con moderación
├── config/           # URLs, WSGI, ASGI
├── settings/         # base.py, local.py, production.py
├── templates/        # Plantillas HTML
├── static/           # CSS, JS, imágenes estáticas
├── theme/            # App de Tailwind CSS
├── requirements/     # base.txt, local.txt, production.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```
