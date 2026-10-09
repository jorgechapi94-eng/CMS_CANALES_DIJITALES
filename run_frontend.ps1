Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  Frontend (Vue + Vite)" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

Set-Location -Path "$PSScriptRoot\frontend"

Write-Host "Verificando dependencias..." -ForegroundColor Yellow
if (-not (Test-Path "node_modules")) {
    Write-Host "Instalando npm packages..." -ForegroundColor Yellow
    npm install
}

Write-Host ""
Write-Host "Iniciando en http://localhost:5173" -ForegroundColor Green
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow
Write-Host ""

npm run dev
