#!/bin/bash

###############################################################################
# Script de Setup Inicial - VM Linux
# Configura ambiente para CargoSnap ICTSI
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
echo -e "${CYAN}     ⚙️  Setup Inicial - CargoSnap ICTSI (VM Linux)${NC}"
echo -e "${CYAN}=============================================================${NC}"
echo ""

# Verificar se é root ou sudo
if [ "$EUID" -eq 0 ]; then 
    echo -e "${YELLOW}⚠️  Não execute este script como root. Use seu usuário normal.${NC}"
    echo -e "${YELLOW}   O script pedirá senha quando necessário.${NC}"
    exit 1
fi

###############################################################################
# 1. ATUALIZAR SISTEMA
###############################################################################
echo -e "${BLUE}[1/8] Atualizando sistema...${NC}"
sudo apt-get update
sudo apt-get upgrade -y
echo -e "${GREEN}  ✓ Sistema atualizado${NC}"

###############################################################################
# 2. INSTALAR PYTHON
###############################################################################
echo ""
echo -e "${BLUE}[2/8] Instalando Python 3 e dependências...${NC}"
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev

echo -e "${GREEN}  ✓ Python instalado: $(python3 --version)${NC}"

###############################################################################
# 3. INSTALAR NODE.JS
###############################################################################
echo ""
echo -e "${BLUE}[3/8] Instalando Node.js...${NC}"

# Verificar se Node já está instalado
if command -v node &> /dev/null; then
    echo -e "${GREEN}  ✓ Node.js já instalado: $(node --version)${NC}"
else
    # Instalar Node.js 20.x (LTS)
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
    echo -e "${GREEN}  ✓ Node.js instalado: $(node --version)${NC}"
fi

echo -e "${GREEN}  ✓ npm instalado: $(npm --version)${NC}"

###############################################################################
# 4. INSTALAR POSTGRESQL (Opcional)
###############################################################################
echo ""
echo -e "${BLUE}[4/8] Verificando PostgreSQL...${NC}"

if command -v psql &> /dev/null; then
    echo -e "${GREEN}  ✓ PostgreSQL já instalado${NC}"
else
    read -p "Deseja instalar PostgreSQL? (s/n): " install_pg
    if [ "$install_pg" = "s" ]; then
        sudo apt-get install -y postgresql postgresql-contrib
        sudo systemctl start postgresql
        sudo systemctl enable postgresql
        echo -e "${GREEN}  ✓ PostgreSQL instalado${NC}"
    else
        echo -e "${YELLOW}  ⚠ PostgreSQL não instalado (usando SQLite)${NC}"
    fi
fi

###############################################################################
# 5. INSTALAR NGINX (Opcional)
###############################################################################
echo ""
echo -e "${BLUE}[5/8] Verificando Nginx...${NC}"

if command -v nginx &> /dev/null; then
    echo -e "${GREEN}  ✓ Nginx já instalado${NC}"
else
    read -p "Deseja instalar Nginx para produção? (s/n): " install_nginx
    if [ "$install_nginx" = "s" ]; then
        sudo apt-get install -y nginx
        sudo systemctl start nginx
        sudo systemctl enable nginx
        echo -e "${GREEN}  ✓ Nginx instalado${NC}"
    else
        echo -e "${YELLOW}  ⚠ Nginx não instalado${NC}"
    fi
fi

###############################################################################
# 6. INSTALAR FERRAMENTAS ÚTEIS
###############################################################################
echo ""
echo -e "${BLUE}[6/8] Instalando ferramentas úteis...${NC}"

sudo apt-get install -y \
    git \
    curl \
    wget \
    vim \
    htop \
    lsof \
    net-tools \
    supervisor

echo -e "${GREEN}  ✓ Ferramentas instaladas${NC}"

###############################################################################
# 7. CONFIGURAR FIREWALL (UFW)
###############################################################################
echo ""
echo -e "${BLUE}[7/8] Configurando firewall...${NC}"

if command -v ufw &> /dev/null; then
    sudo ufw allow 22/tcp      # SSH
    sudo ufw allow 8501/tcp    # Backend
    sudo ufw allow 3000/tcp    # Frontend (dev)
    sudo ufw allow 80/tcp      # HTTP
    sudo ufw allow 443/tcp     # HTTPS
    
    # Não ativa automaticamente para não bloquear SSH
    echo -e "${YELLOW}  ⚠ Firewall configurado mas NÃO ativado${NC}"
    echo -e "${YELLOW}    Para ativar: sudo ufw enable${NC}"
else
    echo -e "${YELLOW}  ⚠ UFW não disponível${NC}"
fi

###############################################################################
# 8. CONFIGURAR PROJETO
###############################################################################
echo ""
echo -e "${BLUE}[8/8] Configurando projeto...${NC}"

PROJECT_DIR="$HOME/projetos/CargoSnap-ICTSI"

if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}  ⚠ Diretório do projeto não encontrado: $PROJECT_DIR${NC}"
    echo -e "${YELLOW}    Clone o repositório primeiro${NC}"
else
    cd "$PROJECT_DIR"
    
    # Tornar scripts executáveis
    chmod +x start-dev.sh
    chmod +x stop-dev.sh
    chmod +x setup-vm.sh
    
    echo -e "${GREEN}  ✓ Scripts configurados como executáveis${NC}"
fi

###############################################################################
# RESUMO
###############################################################################
echo ""
echo -e "${CYAN}=============================================================${NC}"
echo -e "${GREEN}  ✓ Setup Completo!${NC}"
echo -e "${CYAN}=============================================================${NC}"
echo ""
echo -e "${YELLOW}Próximos passos:${NC}"
echo ""
echo -e "  ${CYAN}1.${NC} Navegue até o diretório do projeto:"
echo -e "     ${GREEN}cd ~/projetos/CargoSnap-ICTSI${NC}"
echo ""
echo -e "  ${CYAN}2.${NC} Configure as variáveis de ambiente:"
echo -e "     ${GREEN}cp frontend/.env.example frontend/.env${NC}"
echo -e "     ${GREEN}nano frontend/.env${NC}  # Editar se necessário"
echo ""
echo -e "  ${CYAN}3.${NC} Configure o banco de dados (backend/config/settings.py)"
echo ""
echo -e "  ${CYAN}4.${NC} Execute as migrações:"
echo -e "     ${GREEN}cd backend${NC}"
echo -e "     ${GREEN}python3 -m venv venv${NC}"
echo -e "     ${GREEN}source venv/bin/activate${NC}"
echo -e "     ${GREEN}pip install -r requirements.txt${NC}"
echo -e "     ${GREEN}python manage.py migrate${NC}"
echo -e "     ${GREEN}python manage.py createsuperuser${NC}"
echo ""
echo -e "  ${CYAN}5.${NC} Inicie o projeto:"
echo -e "     ${GREEN}cd ~/projetos/CargoSnap-ICTSI${NC}"
echo -e "     ${GREEN}./start-dev.sh${NC}"
echo ""
echo -e "${YELLOW}URLs de acesso:${NC}"
echo -e "  Backend:  ${CYAN}http://SEU_IP:8501${NC}"
echo -e "  Frontend: ${CYAN}http://SEU_IP:3000${NC}"
echo ""
echo -e "${CYAN}=============================================================${NC}"
