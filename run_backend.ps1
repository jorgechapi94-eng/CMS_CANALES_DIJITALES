Write-Host "===================================" -ForegroundColor Cyan
Write-Host "  Backend (Flask/Python)" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

Set-Location -Path "$PSScriptRoot\backend"

Write-Host "Instalando dependencias..." -ForegroundColor Yellow
pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org -r requirements.txt

Write-Host ""
Write-Host "Configurando entorno..." -ForegroundColor Cyan
$env:FLASK_APP = "app"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"

Write-Host "Inicializando base de datos..." -ForegroundColor Yellow
python init_db.py

Write-Host ""
Write-Host "Iniciando Flask en http://localhost:5000" -ForegroundColor Green
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow
Write-Host ""

flask run --host=0.0.0.0 --port=5000
