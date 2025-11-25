#!/bin/bash

###############################################################################
# Script para Parar Serviços - CargoSnap ICTSI
###############################################################################

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}=============================================================${NC}"
echo -e "${CYAN}     🛑 Parando Serviços CargoSnap ICTSI${NC}"
echo -e "${CYAN}=============================================================${NC}"
echo ""

# Função para matar processo por PID file
kill_by_pidfile() {
    local pidfile=$1
    local name=$2
    
    if [ -f "$pidfile" ]; then
        PID=$(cat "$pidfile")
        if ps -p $PID > /dev/null 2>&1; then
            echo -e "${YELLOW}► Parando $name (PID: $PID)...${NC}"
            kill $PID 2>/dev/null || kill -9 $PID 2>/dev/null
            rm -f "$pidfile"
            echo -e "${GREEN}  ✓ $name parado${NC}"
        else
            echo -e "${YELLOW}  ⚠ $name já estava parado${NC}"
            rm -f "$pidfile"
        fi
    else
        echo -e "${YELLOW}  ⚠ PID file de $name não encontrado${NC}"
    fi
}

# Matar por porta (backup)
kill_by_port() {
    local port=$1
    local name=$2
    
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}► Parando processos na porta $port ($name)...${NC}"
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
        echo -e "${GREEN}  ✓ Porta $port liberada${NC}"
    fi
}

# Parar Backend
echo -e "${YELLOW}[1/2] Parando Backend...${NC}"
kill_by_pidfile "/tmp/cargosnap_backend.pid" "Backend Django"
kill_by_port 8501 "Backend"

# Parar Frontend
echo ""
echo -e "${YELLOW}[2/2] Parando Frontend...${NC}"
kill_by_pidfile "/tmp/cargosnap_frontend.pid" "Frontend React"
kill_by_port 3000 "Frontend"

echo ""
echo -e "${CYAN}=============================================================${NC}"
echo -e "${GREEN}  ✓ Todos os serviços foram parados!${NC}"
echo -e "${CYAN}=============================================================${NC}"
echo ""
