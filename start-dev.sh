#!/bin/bash

###############################################################################
# Script de Inicialização - CargoSnap ICTSI
# Executa backend (porta 8501) e frontend (porta 3000) em desenvolvimento
###############################################################################

set -e  # Exit on error

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Diretório raiz do projeto
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="${PROJECT_ROOT}/backend"
FRONTEND_DIR="${PROJECT_ROOT}/frontend"

# Configurações
BACKEND_PORT=8501
FRONTEND_PORT=3000

echo -e "${CYAN}=============================================================${NC}"
echo -e "${CYAN}     🚀 CargoSnap ICTSI - Iniciando Ambiente Dev${NC}"
echo -e "${CYAN}=============================================================${NC}"
echo ""

###############################################################################
# Função para verificar se uma porta está em uso
###############################################################################
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        return 0  # Porta em uso
    else
        return 1  # Porta livre
    fi
}

###############################################################################
# Função para matar processo em uma porta
###############################################################################
kill_port() {
    local port=$1
    echo -e "${YELLOW}► Liberando porta $port...${NC}"
    lsof -ti:$port | xargs kill -9 2>/dev/null || true
    sleep 1
}

###############################################################################
# 1. VERIFICAR DEPENDÊNCIAS
###############################################################################
echo -e "${BLUE}[1/6] Verificando dependências...${NC}"

# Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 não encontrado!${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ Python 3: $(python3 --version)${NC}"

# Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}✗ Node.js não encontrado!${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ Node.js: $(node --version)${NC}"

# npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}✗ npm não encontrado!${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ npm: $(npm --version)${NC}"

###############################################################################
# 2. CONFIGURAR BACKEND
###############################################################################
echo ""
echo -e "${BLUE}[2/6] Configurando Backend (Django)...${NC}"

cd "$BACKEND_DIR"

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}  ► Criando ambiente virtual...${NC}"
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo -e "${YELLOW}  ► Ativando ambiente virtual...${NC}"
source venv/bin/activate

# Instalar dependências
if [ ! -f "venv/.deps_installed" ]; then
    echo -e "${YELLOW}  ► Instalando dependências Python...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt
    touch venv/.deps_installed
else
    echo -e "${GREEN}  ✓ Dependências Python já instaladas${NC}"
fi

# Executar migrações
echo -e "${YELLOW}  ► Aplicando migrações do banco...${NC}"
python manage.py migrate --noinput

# Coletar arquivos estáticos (para produção)
# echo -e "${YELLOW}  ► Coletando arquivos estáticos...${NC}"
# python manage.py collectstatic --noinput

echo -e "${GREEN}  ✓ Backend configurado${NC}"

###############################################################################
# 3. CONFIGURAR FRONTEND
###############################################################################
echo ""
echo -e "${BLUE}[3/6] Configurando Frontend (React)...${NC}"

cd "$FRONTEND_DIR"

# Instalar dependências
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}  ► Instalando dependências Node.js...${NC}"
    npm install
else
    echo -e "${GREEN}  ✓ Dependências Node.js já instaladas${NC}"
fi

# Verificar arquivo .env
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo -e "${YELLOW}  ► Criando arquivo .env...${NC}"
        cp .env.example .env
        # Atualizar porta do backend
        sed -i "s|VITE_API_URL=.*|VITE_API_URL=http://localhost:${BACKEND_PORT}/api|g" .env
    else
        echo -e "${RED}  ✗ Arquivo .env.example não encontrado!${NC}"
    fi
else
    echo -e "${GREEN}  ✓ Arquivo .env existe${NC}"
fi

echo -e "${GREEN}  ✓ Frontend configurado${NC}"

###############################################################################
# 4. LIBERAR PORTAS
###############################################################################
echo ""
echo -e "${BLUE}[4/6] Verificando portas...${NC}"

if check_port $BACKEND_PORT; then
    echo -e "${YELLOW}  ⚠ Porta $BACKEND_PORT em uso${NC}"
    kill_port $BACKEND_PORT
fi

if check_port $FRONTEND_PORT; then
    echo -e "${YELLOW}  ⚠ Porta $FRONTEND_PORT em uso${NC}"
    kill_port $FRONTEND_PORT
fi

echo -e "${GREEN}  ✓ Portas liberadas${NC}"

###############################################################################
# 5. INICIAR BACKEND
###############################################################################
echo ""
echo -e "${BLUE}[5/6] Iniciando Backend...${NC}"

cd "$BACKEND_DIR"
source venv/bin/activate

# Criar diretório de logs se não existir
mkdir -p logs

echo -e "${YELLOW}  ► Iniciando Django na porta ${BACKEND_PORT}...${NC}"
nohup python manage.py runserver 0.0.0.0:$BACKEND_PORT > logs/django.log 2>&1 &
BACKEND_PID=$!

# Salvar PID
echo $BACKEND_PID > /tmp/cargosnap_backend.pid

# Aguardar backend iniciar
echo -e "${YELLOW}  ► Aguardando backend iniciar...${NC}"
sleep 5

if ps -p $BACKEND_PID > /dev/null; then
    echo -e "${GREEN}  ✓ Backend rodando (PID: $BACKEND_PID)${NC}"
    echo -e "${GREEN}  ✓ URL: http://localhost:${BACKEND_PORT}${NC}"
else
    echo -e "${RED}  ✗ Falha ao iniciar backend${NC}"
    echo -e "${RED}  ✗ Verifique logs em: ${BACKEND_DIR}/logs/django.log${NC}"
    exit 1
fi

###############################################################################
# 6. INICIAR FRONTEND
###############################################################################
echo ""
echo -e "${BLUE}[6/6] Iniciando Frontend...${NC}"

cd "$FRONTEND_DIR"

echo -e "${YELLOW}  ► Iniciando React na porta ${FRONTEND_PORT}...${NC}"
nohup npm run dev -- --host 0.0.0.0 --port $FRONTEND_PORT > ../backend/logs/vite.log 2>&1 &
FRONTEND_PID=$!

# Salvar PID
echo $FRONTEND_PID > /tmp/cargosnap_frontend.pid

# Aguardar frontend iniciar
echo -e "${YELLOW}  ► Aguardando frontend iniciar...${NC}"
sleep 8

if ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${GREEN}  ✓ Frontend rodando (PID: $FRONTEND_PID)${NC}"
    echo -e "${GREEN}  ✓ URL: http://localhost:${FRONTEND_PORT}${NC}"
else
    echo -e "${RED}  ✗ Falha ao iniciar frontend${NC}"
    echo -e "${RED}  ✗ Verifique logs em: ${BACKEND_DIR}/logs/vite.log${NC}"
fi

###############################################################################
# RESUMO
###############################################################################
echo ""
echo -e "${CYAN}=============================================================${NC}"
echo -e "${GREEN}  ✓ Ambiente CargoSnap ICTSI iniciado!${NC}"
echo -e "${CYAN}=============================================================${NC}"
echo ""
echo -e "${PURPLE}📊 Serviços:${NC}"
echo -e "  ${CYAN}Backend (Django):${NC}  http://localhost:${BACKEND_PORT}"
echo -e "  ${CYAN}Frontend (React):${NC} http://localhost:${FRONTEND_PORT}"
echo -e "  ${CYAN}Admin Django:${NC}     http://localhost:${BACKEND_PORT}/admin"
echo -e "  ${CYAN}API Docs:${NC}         http://localhost:${BACKEND_PORT}/api"
echo ""
echo -e "${PURPLE}📝 PIDs:${NC}"
echo -e "  Backend:  $BACKEND_PID"
echo -e "  Frontend: $FRONTEND_PID"
echo ""
echo -e "${PURPLE}📁 Logs:${NC}"
echo -e "  Backend:  ${BACKEND_DIR}/logs/django.log"
echo -e "  Frontend: ${BACKEND_DIR}/logs/vite.log"
echo ""
echo -e "${YELLOW}Para parar os serviços, execute:${NC}"
echo -e "  ${CYAN}./stop-dev.sh${NC}"
echo ""
echo -e "${YELLOW}Para ver logs em tempo real:${NC}"
echo -e "  ${CYAN}tail -f ${BACKEND_DIR}/logs/django.log${NC}"
echo -e "  ${CYAN}tail -f ${BACKEND_DIR}/logs/vite.log${NC}"
echo ""
echo -e "${CYAN}=============================================================${NC}"
