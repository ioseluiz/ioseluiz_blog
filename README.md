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
| Animaciones | matplotlib FuncAnimation → HTML iframe |

## Funcionalidades

- **Posts** en Markdown con soporte de fórmulas matemáticas (`$...$`, `$$...$$`), snippets de código con syntax highlighting e imágenes incrustadas
- **Animaciones interactivas** generadas con matplotlib (`FuncAnimation`) embebidas como `<iframe>` en el cuerpo del post
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

## Animaciones interactivas (matplotlib)

Es posible incrustar animaciones de matplotlib directamente en el cuerpo de un post usando `FuncAnimation.to_jshtml()`. El archivo resultante es HTML autocontenido con controles play/pause/loop. El flujo completo es:

### 1. Generar la animación en Python (en tu máquina local)

```python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig, ax = plt.subplots()
x = np.linspace(0, 2 * np.pi, 300)
line, = ax.plot(x, np.sin(x))

def update(frame):
    line.set_ydata(np.sin(x + frame / 10))
    return (line,)

anim = animation.FuncAnimation(fig, update, frames=100, interval=50, blit=True)

# Guardar como HTML autocontenido
with open("mi_animacion.html", "w") as f:
    f.write(anim.to_jshtml())

plt.close()
```

Dependencias necesarias localmente:

```bash
pip install matplotlib numpy
```

### 2. Subir la animación desde el admin

1. Ir a `/admin/` → **Animaciones** → **Añadir animación**
2. Completar el título y seleccionar el archivo `.html` generado
3. Guardar — el campo **Código iframe** aparece con el HTML listo para copiar

### 3. Incrustar en el post

En el editor Markdown del post, pegar el código iframe copiado del admin:

```html
<iframe src="/media/animations/mi_animacion.html" width="700" height="500" frameborder="0" allowfullscreen></iframe>
```

El Markdown del blog acepta HTML directo, por lo que el `<iframe>` se renderiza sin ninguna configuración adicional.

> **Nota sobre tamaño**: `to_jshtml()` incrusta cada frame como imagen base64 dentro del HTML. Una animación de 100 frames en 720p puede pesar varios MB. Para posts públicos conviene mantener frames ≤ 100 y resolución moderada (`figsize=(8, 4)`, `dpi=80`).

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
