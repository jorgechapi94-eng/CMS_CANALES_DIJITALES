# Portal Web Institucional UPEC & CMS a Medida

> Sistema de gestión de contenido (CMS) y portal público para la Universidad Politécnica Estatal del Carchi (UPEC). Incluye noticias, periódicos digitales, programas académicos, y streaming de radio/TV en vivo.

---

## ️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│  Nginx (Puerto 80/443)                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │ /        │  │ /api/*   │  │ /uploads │  │/radio- │  │
│  │ Vue SPA  │  │ Flask API│  │ Estáticos│  │stream/ │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘  │
└─────────────────────────────────────────────────────────┘
         │              │                         │
    Vue 3 + Vite    Flask + Gunicorn         Icecast :8000
                        │
                   MySQL 8.0
```

## 🚀 Inicio Rápido (Desarrollo Local)

### Prerrequisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (incluye Docker Compose)
- [Node.js 20+](https://nodejs.org/) (para desarrollo frontend sin Docker)
- [Python 3.11+](https://www.python.org/) (para desarrollo backend sin Docker)
- [Git](https://git-scm.com/)

### Opción 1: Docker Compose (Recomendada)

```bash
# 1. Clonar el repositorio
git clone <repo-url> Radio_CMS
cd Radio_CMS

# 2. Configurar variables de entorno
cp backend/.env.example backend/.env
# Editar backend/.env con sus credenciales

# 3. Levantar todos los servicios
docker-compose up --build

# 4. Acceder al portal
# Frontend:  http://localhost:5173
# API:       http://localhost:5000/api
# Nginx:     http://localhost:80
```

### Opción 2: Desarrollo Local (Sin Docker)

#### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con la URL de tu MySQL local

# Inicializar base de datos
flask db init
flask db migrate -m "initial"
flask db upgrade

# Crear datos iniciales (roles + admin)
python -c "from app.seeds.initial_data import seed_all; seed_all()"

# Ejecutar servidor de desarrollo
flask run --port 5000 --debug
```

#### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev

# Abrir http://localhost:5173
```

## 🔐 Credenciales por Defecto

| Rol | Email | Contraseña |
|:----|:------|:-----------|
| SuperAdmin | `admin@upec.edu.ec` | `Admin2024!` |

> ⚠️ **Cambiar la contraseña inmediatamente** después del primer inicio de sesión.

## 📁 Estructura del Proyecto

```
Radio_CMS/
├── backend/              # API REST (Flask + Python)
│   ├── app/
│   │   ├── __init__.py   # Application Factory
│   │   ├── config.py     # Configuraciones
│   │   ├── extensions.py # SQLAlchemy, JWT, CORS
│   │   ├── models/       # Modelos de datos
│   │   ├── api/          # Endpoints REST (Blueprints)
│   │   ├── utils/        # Decoradores, validadores
│   │   └── seeds/        # Datos iniciales
│   ├── migrations/       # Migraciones Alembic
│   ├── uploads/          # PDFs e imágenes
│   ├── tests/            # Tests pytest
│   └── requirements.txt
│
├── frontend/             # SPA (Vue 3 + Vite + TypeScript)
│   ├── src/
│   │   ├── App.vue       # Shell global + Audio Player
│   │   ├── router/       # Rutas públicas y admin
│   │   ├── stores/       # Estado Pinia (auth, audio, ui)
│   │   ├── components/   # Componentes reutilizables
│   │   ├── views/        # Páginas (public/ y admin/)
│   │   └── composables/  # Lógica compartida
│   └── tailwind.config.js
│
├── nginx/                # Configuración Nginx
├── docker-compose.yml    # Orquestación Docker
├── Dockerfile.backend
└── Dockerfile.frontend
```

## 🎨 Paleta de Colores Institucional

| Color | Código | Uso |
|:------|:-------|:----|
| Verde UPEC | `#006633` | Color primario, headers, botones principales |
| Amarillo UPEC | `#FFCE00` | Acentos, badges, CTAs secundarios |
| Verde Oscuro | `#004d26` | Footer, hover states |
| Verde Claro | `#00994d` | Badges, estados activos |

## 🔌 API Endpoints

### Autenticación
- `POST /api/auth/login` — Iniciar sesión (requiere email @upec.edu.ec)
- `POST /api/auth/refresh` — Renovar token
- `GET /api/auth/me` — Usuario actual
- `POST /api/auth/logout` — Cerrar sesión

### Noticias
- `GET /api/news` — Listar noticias publicadas
- `GET /api/news/:slug` — Detalle por slug
- `POST /api/news` — Crear (Editor/SuperAdmin)
- `PUT /api/news/:id` — Actualizar
- `DELETE /api/news/:id` — Archivar

### Periódicos
- `GET /api/newspapers` — Listar periódicos
- `POST /api/newspapers` — Subir PDF (Editor/SuperAdmin)
- `PUT /api/newspapers/:id` — Actualizar
- `DELETE /api/newspapers/:id` — Eliminar

### Programas Académicos
- `GET /api/programs` — Listar programas
- `GET /api/programs/:id` — Detalle con docentes/estudiantes/proyectos
- `POST /api/programs` — Crear (GestorProgramas/SuperAdmin)
- `PUT /api/programs/:id` — Actualizar
- `DELETE /api/programs/:id` — Desactivar

### Archivos
- `POST /api/uploads/image` — Subir imagen
- `POST /api/uploads/pdf` — Subir PDF

### Integraciones
- `GET /api/youtube/latest` — Videos recientes (cache 30 min)
- `GET /api/radio/status` — Estado del stream Icecast

## 🧪 Testing

```bash
# Backend
cd backend
python -m pytest tests/ -v --cov=app

# Frontend
cd frontend
npm run test:unit
```

## 📋 Variables de Entorno

Copiar `backend/.env.example` a `backend/.env` y configurar:

| Variable | Descripción | Ejemplo |
|:---------|:------------|:--------|
| `DATABASE_URL` | URI de conexión MySQL | `mysql+pymysql://root:pass@localhost/upec_cms_db` |
| `SECRET_KEY` | Clave secreta Flask | (generar aleatoria) |
| `JWT_SECRET_KEY` | Clave secreta JWT | (generar aleatoria) |
| `YOUTUBE_API_KEY` | API Key de YouTube Data v3 | `AIza...` |
| `YOUTUBE_CHANNEL_ID` | ID del canal UPEC | `UCxxxxxxx` |
| `ICECAST_STATUS_URL` | URL status Icecast | `http://localhost:8000/status-json.xsl` |

## 🚢 Despliegue a Producción

1. Configurar variables de entorno de producción
2. Cambiar `FLASK_CONFIG=production`
3. Generar claves secretas seguras para `SECRET_KEY` y `JWT_SECRET_KEY`
4. Configurar certificado SSL (Let's Encrypt) en Nginx
5. Ejecutar: `docker-compose -f docker-compose.yml up -d --build`

## 📄 Licencia

Desarrollo a medida para la Universidad Politécnica Estatal del Carchi (UPEC).
Todos los derechos reservados.
