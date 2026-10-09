Write-Host "========================================" -ForegroundColor Magenta
Write-Host "   DEMO LOCAL - Radio CMS UPEC" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta
Write-Host ""

Write-Host "Verificando requisitos..." -ForegroundColor Cyan
Write-Host ""

$nodeOk = $false
$pythonOk = $false

try {
    $nodeVersion = node --version
    Write-Host "OK - Node.js: $nodeVersion" -ForegroundColor Green
    $nodeOk = $true
} catch {
    Write-Host "ERROR - Node.js NO INSTALADO" -ForegroundColor Red
}

try {
    $pythonVersion = python --version
    Write-Host "OK - Python: $pythonVersion" -ForegroundColor Green
    $pythonOk = $true
} catch {
    Write-Host "ERROR - Python NO INSTALADO" -ForegroundColor Red
}

Write-Host ""

if (-not $nodeOk -or -not $pythonOk) {
    Write-Host "INSTALACION REQUERIDA" -ForegroundColor Red
    Write-Host ""
    if (-not $nodeOk) {
        Write-Host "1. Descarga Node.js: https://nodejs.org/" -ForegroundColor Yellow
    }
    if (-not $pythonOk) {
        Write-Host "2. Descarga Python: https://www.python.org/" -ForegroundColor Yellow
    }
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "Todos los requisitos OK" -ForegroundColor Green
Write-Host ""
Write-Host "Opciones:" -ForegroundColor Cyan
Write-Host "1 - Frontend + Backend" -ForegroundColor White
Write-Host "2 - Solo Frontend" -ForegroundColor White
Write-Host "3 - Solo Backend" -ForegroundColor White
Write-Host ""

$opcion = Read-Host "Elige opcion"

if ($opcion -eq "1") {
    Write-Host "Iniciando Frontend y Backend..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-File", "$PSScriptRoot\run_frontend.ps1"
    Start-Sleep -Seconds 2
    Start-Process powershell -ArgumentList "-NoExit", "-File", "$PSScriptRoot\run_backend.ps1"
    Write-Host "Iniciado. Frontend: http://localhost:5173" -ForegroundColor Green
    Write-Host "Backend: http://localhost:5000" -ForegroundColor Green
}
elseif ($opcion -eq "2") {
    Write-Host "Iniciando Frontend..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-File", "$PSScriptRoot\run_frontend.ps1"
}
elseif ($opcion -eq "3") {
    Write-Host "Iniciando Backend..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-File", "$PSScriptRoot\run_backend.ps1"
}
else {
    Write-Host "Opcion invalida" -ForegroundColor Red
}

Read-Host "Presiona Enter para cerrar"
