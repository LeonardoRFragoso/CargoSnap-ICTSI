#!/bin/bash

###############################################################################
# Script de Instalação dos Serviços Systemd - CargoSnap ICTSI
# Configura backend e frontend como serviços do sistema
###############################################################################

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}=============================================================${NC}"
echo -e "${CYAN}  📦 Instalando Serviços Systemd - CargoSnap ICTSI${NC}"
echo -e "${CYAN}=============================================================${NC}"
echo ""

# Diretório do projeto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

###############################################################################
# 1. PARAR PROCESSOS EXISTENTES
###############################################################################
echo -e "${BLUE}[1/7] Parando processos existentes...${NC}"

if [ -f "$PROJECT_DIR/stop-dev.sh" ]; then
    $PROJECT_DIR/stop-dev.sh || true
fi

# Matar processos nas portas
lsof -ti:8501 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

echo -e "${GREEN}  ✓ Processos parados${NC}"

###############################################################################
# 2. CRIAR .ENV DE PRODUÇÃO
###############################################################################
echo ""
echo -e "${BLUE}[2/7] Configurando variáveis de ambiente...${NC}"

if [ ! -f "$PROJECT_DIR/backend/.env" ]; then
    cp "$PROJECT_DIR/backend/.env.production" "$PROJECT_DIR/backend/.env"
    echo -e "${GREEN}  ✓ Arquivo .env criado${NC}"
else
    echo -e "${YELLOW}  ⚠ Arquivo .env já existe${NC}"
fi

###############################################################################
# 3. COPIAR ARQUIVOS DE SERVIÇO
###############################################################################
echo ""
echo -e "${BLUE}[3/7] Instalando arquivos de serviço...${NC}"

sudo cp "$PROJECT_DIR/cargosnap-backend.service" /etc/systemd/system/
sudo cp "$PROJECT_DIR/cargosnap-frontend.service" /etc/systemd/system/

echo -e "${GREEN}  ✓ Arquivos copiados para /etc/systemd/system/${NC}"

###############################################################################
# 4. RECARREGAR SYSTEMD
###############################################################################
echo ""
echo -e "${BLUE}[4/7] Recarregando systemd...${NC}"

sudo systemctl daemon-reload

echo -e "${GREEN}  ✓ Systemd recarregado${NC}"

###############################################################################
# 5. HABILITAR SERVIÇOS
###############################################################################
echo ""
echo -e "${BLUE}[5/7] Habilitando serviços para iniciar no boot...${NC}"

sudo systemctl enable cargosnap-backend.service
sudo systemctl enable cargosnap-frontend.service

echo -e "${GREEN}  ✓ Serviços habilitados${NC}"

###############################################################################
# 6. INICIAR SERVIÇOS
###############################################################################
echo ""
echo -e "${BLUE}[6/7] Iniciando serviços...${NC}"

sudo systemctl start cargosnap-backend.service
sleep 3
sudo systemctl start cargosnap-frontend.service
sleep 3

echo -e "${GREEN}  ✓ Serviços iniciados${NC}"

###############################################################################
# 7. VERIFICAR STATUS
###############################################################################
echo ""
echo -e "${BLUE}[7/7] Verificando status dos serviços...${NC}"

BACKEND_STATUS=$(systemctl is-active cargosnap-backend.service)
FRONTEND_STATUS=$(systemctl is-active cargosnap-frontend.service)

if [ "$BACKEND_STATUS" = "active" ]; then
    echo -e "${GREEN}  ✓ Backend: ATIVO${NC}"
else
    echo -e "${RED}  ✗ Backend: $BACKEND_STATUS${NC}"
fi

if [ "$FRONTEND_STATUS" = "active" ]; then
    echo -e "${GREEN}  ✓ Frontend: ATIVO${NC}"
else
    echo -e "${RED}  ✗ Frontend: $FRONTEND_STATUS${NC}"
fi

###############################################################################
# RESUMO
###############################################################################
echo ""
echo -e "${CYAN}=============================================================${NC}"
echo -e "${GREEN}  ✓ Instalação Concluída!${NC}"
echo -e "${CYAN}=============================================================${NC}"
echo ""
echo -e "${YELLOW}📊 Serviços instalados:${NC}"
echo -e "  • ${CYAN}cargosnap-backend.service${NC}  - Django na porta 8501"
echo -e "  • ${CYAN}cargosnap-frontend.service${NC} - React na porta 3000"
echo ""
echo -e "${YELLOW}🌐 URLs de acesso:${NC}"
echo -e "  • Frontend:  ${CYAN}http://192.168.0.45:3000${NC}"
echo -e "  • Backend:   ${CYAN}http://192.168.0.45:8501${NC}"
echo -e "  • Admin:     ${CYAN}http://192.168.0.45:8501/admin${NC}"
echo ""
echo -e "${YELLOW}📝 Comandos úteis:${NC}"
echo -e "  ${CYAN}# Ver status${NC}"
echo -e "  sudo systemctl status cargosnap-backend"
echo -e "  sudo systemctl status cargosnap-frontend"
echo ""
echo -e "  ${CYAN}# Parar serviços${NC}"
echo -e "  sudo systemctl stop cargosnap-backend"
echo -e "  sudo systemctl stop cargosnap-frontend"
echo ""
echo -e "  ${CYAN}# Iniciar serviços${NC}"
echo -e "  sudo systemctl start cargosnap-backend"
echo -e "  sudo systemctl start cargosnap-frontend"
echo ""
echo -e "  ${CYAN}# Reiniciar serviços${NC}"
echo -e "  sudo systemctl restart cargosnap-backend"
echo -e "  sudo systemctl restart cargosnap-frontend"
echo ""
echo -e "  ${CYAN}# Ver logs${NC}"
echo -e "  sudo journalctl -u cargosnap-backend -f"
echo -e "  sudo journalctl -u cargosnap-frontend -f"
echo ""
echo -e "  ${CYAN}# Desabilitar serviços${NC}"
echo -e "  sudo systemctl disable cargosnap-backend"
echo -e "  sudo systemctl disable cargosnap-frontend"
echo ""
echo -e "${CYAN}=============================================================${NC}"
