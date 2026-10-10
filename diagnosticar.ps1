Write-Host "Diagnosticando el backend..." -ForegroundColor Cyan
Write-Host ""

cd c:\Users\Usuario\Documents\Radio_CMS\backend

Write-Host "1. Verificando si Flask esta corriendo..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000" -ErrorAction Stop
    Write-Host "OK - Backend corriendo" -ForegroundColor Green
} catch {
    Write-Host "ERROR - Backend no responde" -ForegroundColor Red
    Read-Host "Presiona Enter"
    exit 1
}

Write-Host ""
Write-Host "2. Intentando login..." -ForegroundColor Yellow

$loginData = @{
    email = "admin@upec.edu.ec"
    password = "admin123"
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/auth/login" -Method POST -Body $loginData -ContentType "application/json"
    Write-Host "OK - Login exitoso" -ForegroundColor Green
    $response.Content
} catch {
    Write-Host "ERROR - Login fallo: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    Write-Host $_.Exception.Response
}

Write-Host ""
Read-Host "Presiona Enter para cerrar"
