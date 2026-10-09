# Guía de Instalación para Demo Local - Radio CMS

## Requisitos Previos

### 1. Instalar Node.js (para el Frontend)
1. Visita: https://nodejs.org/
2. Descarga la versión **LTS** (versión estable recomendada)
3. Ejecuta el instalador `node-vXX.X.X-x64.msi`
4. Sigue el asistente de instalación (deja las opciones por defecto)
5. **Reinicia PowerShell** después de instalar

**Verificar instalación:**
```powershell
node --version
npm --version
```

### 2. Instalar Python (para el Backend)
1. Visita: https://www.python.org/downloads/
2. Descarga Python 3.11 o superior
3. **¡IMPORTANTE!** Durante la instalación, marca la casilla **"Add Python to PATH"**
4. Haz clic en "Install Now"
5. **Reinicia PowerShell** después de instalar

**Verificar instalación:**
```powershell
python --version
pip --version
```

---

## Instalación del Proyecto

### Paso 1: Instalar dependencias del Frontend

```powershell
cd c:\Users\Usuario\Documents\Radio_CMS\frontend
npm install
```

### Paso 2: Instalar dependencias del Backend

```powershell
cd c:\Users\Usuario\Documents\Radio_CMS\backend
pip install -r requirements.txt
```

---

## Ejecutar la Demo Local

### Opción A: Usar los scripts automáticos (Más fácil)

#### En Windows PowerShell:

**Terminal 1 - Frontend:**
```powershell
cd c:\Users\Usuario\Documents\Radio_CMS
.\run_frontend.ps1
```

**Terminal 2 - Backend:**
```powershell
cd c:\Users\Usuario\Documents\Radio_CMS
.\run_backend.ps1
```

### Opción B: Ejecutar manualmente

**Terminal 1 - Frontend:**
```powershell
cd c:\Users\Usuario\Documents\Radio_CMS\frontend
npm run dev
```

**Terminal 2 - Backend:**
```powershell
cd c:\Users\Usuario\Documents\Radio_CMS\backend
$env:FLASK_APP="app"
$env:FLASK_ENV="development"
flask run --host=0.0.0.0 --port=5000
```

---

## Acceder a la Aplicación

Una vez que ambos servidores estén corriendo:

- **Frontend:** http://localhost:5173 (o el puerto que indique Vite)
- **Backend API:** http://localhost:5000
- **API Docs:** http://localhost:5000/api/docs (si existe)

---

## Solución de Problemas Comunes

### Error: "npm no se reconoce"
- Node.js no está instalado o no está en el PATH
- Reinicia PowerShell después de instalar Node.js

### Error: "python no se reconoce"
- Python no está instalado o no está en el PATH
- Durante la instalación, asegúrate de marcar "Add Python to PATH"

### Error: Puerto en uso
Si el puerto 5000 o 5173 está ocupado:
```powershell
# Para el frontend, usa otro puerto:
npm run dev -- --port 3000

# Para el backend, usa otro puerto:
flask run --port 5001
```

### Error: "Module not found"
- Asegúrate de haber ejecutado `npm install` en frontend
- Asegúrate de haber ejecutado `pip install -r requirements.txt` en backend

---

## Detener los Servidores

Presiona `Ctrl + C` en cada terminal para detener los servidores.
