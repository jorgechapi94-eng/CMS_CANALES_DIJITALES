Write-Host "Testeando login..." -ForegroundColor Cyan

$loginData = @{
    email = "admin@upec.edu.ec"
    password = "admin123"
} | ConvertTo-Json

Write-Host "Enviando request..." -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/auth/login" -Method POST -Body $loginData -ContentType "application/json"
    Write-Host "OK - Login exitoso" -ForegroundColor Green
    Write-Host $response.Content -ForegroundColor Green
} catch {
    $errorResponse = $_.ErrorDetails.Message
    Write-Host "ERROR - Respuesta del servidor:" -ForegroundColor Red
    Write-Host $errorResponse -ForegroundColor Yellow
}

Read-Host "Presiona Enter"
