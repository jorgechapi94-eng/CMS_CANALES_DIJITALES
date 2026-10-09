# 🔓 Solucionar Error de Ejecución de Scripts en PowerShell

## Error que recibes:
```
No se puede cargar el archivo porque la ejecución de scripts está deshabilitada en este sistema.
```

---

## ✅ Solución (Elige una opción)

### Opción 1: Cambiar Política para el Usuario Actual (Recomendada)

1. **Abre PowerShell como Administrador:**
   - Presiona `Windows + X`
   - Selecciona "Windows PowerShell (Administrador)" o "Terminal (Administrador)"
   - O busca "PowerShell" en el menú inicio, clic derecho → "Ejecutar como administrador"

2. **Ejecuta este comando:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Confirma con:** `S` o `Y` (Sí)

4. **Cierra PowerShell Administrador**

5. **Abre PowerShell normal** en tu carpeta del proyecto y ejecuta:
   ```powershell
   .\run_demo.ps1
   ```

---

### Opción 2: Ejecutar Sin Cambiar Política (Temporal)

Si no puedes o no quieres cambiar la política, ejecuta los comandos directamente:

**En una terminal PowerShell normal:**

```powershell
# Para el Frontend
cd c:\Users\Usuario\Documents\Radio_CMS\frontend
npm install
npm run dev
```

**En OTRA terminal PowerShell:**

```powershell
# Para el Backend
cd c:\Users\Usuario\Documents\Radio_CMS\backend
pip install -r requirements.txt
python init_db.py
$env:FLASK_APP="app"
$env:FLASK_ENV="development"
flask run --port 5000
```

---

### Opción 3: Bypass Temporal (Solo para esta sesión)

**Ejecuta:**
```powershell
powershell -ExecutionPolicy Bypass -File .\run_demo.ps1
```

Este comando permite ejecutar el script sin cambiar la política del sistema permanentemente.

---

## 🔍 Verificar si Funcionó

Después de aplicar la Opción 1, verifica con:
```powershell
Get-ExecutionPolicy -Scope CurrentUser
```

Debe mostrar: **RemoteSigned**

---

## ℹ️ ¿Qué hace RemoteSigned?

- Permite ejecutar scripts creados localmente en tu computadora
- Requiere firma digital solo para scripts descargados de internet
- Es seguro y recomendado para desarrollo

---

## 🚀 Después de Solucionar

Una vez resuelto el problema de permisos, ejecuta:

```powershell
.\run_demo.ps1
```

Y selecciona la opción 1 para iniciar la demo completa.

---

## ❓ Problemas Comunes

### "Acceso denegado" al ejecutar Set-ExecutionPolicy

**Solución:** Asegúrate de estar ejecutando PowerShell **como Administrador**

### El comando funciona pero luego vuelve el error

**Solución:** Reinicia PowerShell después de cambiar la política

### No puedo abrir PowerShell como Administrador

**Solución:** Usa la Opción 2 (ejecutar comandos directamente) o la Opción 3 (Bypass temporal)
