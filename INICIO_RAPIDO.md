# 🚀 Inicio Rápido - Demo Local

## ⚡ Ejecución Rápida (Si ya tienes Node.js y Python)

### Opción 1: Script Automático (Recomendado)

1. Abre PowerShell en esta carpeta
2. Ejecuta:
```powershell
.\run_demo.ps1
```
3. Selecciona la opción 1 (Frontend + Backend)
4. ¡Listo! Se abrirán dos ventanas automáticamente

### Opción 2: Manual

**Terminal 1 - Frontend:**
```powershell
.\run_frontend.ps1
```

**Terminal 2 - Backend:**
```powershell
.\run_backend.ps1
```

---

## 📋 Si es tu primera vez

### Paso 1: Instalar Requisitos

1. **Node.js** → https://nodejs.org/ (versión LTS)
2. **Python** → https://www.python.org/ (marcar "Add to PATH")
3. **Reiniciar PowerShell** después de instalar

### Paso 2: Ejecutar la Demo

```powershell
.\run_demo.ps1
```

---

## 🌐 URLs de Acceso

- **Aplicación Web:** http://localhost:5173
- **API Backend:** http://localhost:5000

---

## ❓ Problemas Comunes

### "No se puede ejecutar scripts en este sistema"

Ejecuta esto en PowerShell como Administrador:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "npm no se reconoce" o "python no se reconoce"

- Asegúrate de haber instalado Node.js y Python
- **IMPORTANTE:** Reinicia PowerShell después de instalar
- Verifica que estén en el PATH del sistema

### Puerto en uso

Si los puertos 5000 o 5173 están ocupados, edita los scripts y cambia los puertos.

---

## 🛑 Detener los Servidores

Presiona `Ctrl + C` en cada ventana de PowerShell, o simplemente cierra las ventanas.

---

## 📚 Más Información

Consulta `SETUP_DEMO_LOCAL.md` para instrucciones detalladas.
