# CargoSnap ICTSI - Setup Script for Windows
# Run with: powershell -ExecutionPolicy Bypass -File setup.ps1

Write-Host "🚀 CargoSnap ICTSI - Automated Setup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "Checking Node.js..." -ForegroundColor Yellow
node --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Node.js not found. Frontend will not be set up." -ForegroundColor Yellow
}

# Backend Setup
Write-Host ""
Write-Host "📦 Setting up Backend..." -ForegroundColor Cyan

Set-Location backend

# Create virtual environment
if (!(Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements-windows.txt

# Create .env if not exists
if (!(Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚠️  Please edit .env file with your database credentials" -ForegroundColor Yellow
}

# Run migrations
Write-Host "Running migrations..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate

# Create companies
Write-Host "Creating default companies..." -ForegroundColor Yellow
python manage.py create_companies

# Populate structures and damages
Write-Host "Populating structures and damage types..." -ForegroundColor Yellow
python manage.py populate_structures_damages

# Create default workflows
Write-Host "Creating default workflows..." -ForegroundColor Yellow
python manage.py create_default_workflows

# Create superuser
Write-Host ""
Write-Host "Create a superuser account:" -ForegroundColor Cyan
python manage.py createsuperuser

Set-Location ..

# Frontend Setup (if Node exists)
if (Get-Command node -ErrorAction SilentlyContinue) {
    Write-Host ""
    Write-Host "📦 Setting up Frontend..." -ForegroundColor Cyan
    Set-Location frontend
    
    Write-Host "Installing npm dependencies..." -ForegroundColor Yellow
    npm install
    
    Set-Location ..
}

Write-Host ""
Write-Host "✅ Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Edit backend/.env with your settings"
Write-Host "  2. Start backend:  cd backend && .\venv\Scripts\Activate.ps1 && python manage.py runserver"
Write-Host "  3. Start frontend: cd frontend && npm run dev"
Write-Host "  4. Access: http://localhost:8000/admin (backend), http://localhost:5173 (frontend)"
Write-Host ""
