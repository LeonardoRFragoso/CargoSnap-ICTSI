#!/bin/bash

###############################################################################
# Configurar TUDO na porta 8501 - Frontend + Backend juntos
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
echo -e "${CYAN}  🔥 CONFIGURANDO TUDO NA PORTA 8501${NC}"
echo -e "${CYAN}=============================================================${NC}"
echo ""

PROJECT_DIR="$HOME/projetos/CargoSnap-ICTSI"

# 1. PARAR SERVIÇOS
echo -e "${BLUE}[1/6] Parando serviços...${NC}"
sudo systemctl stop cargosnap-frontend || true
sudo systemctl stop cargosnap-backend || true
sudo systemctl disable cargosnap-frontend || true
echo -e "${GREEN}  ✓ Serviços parados${NC}"

# 2. BUILD DO FRONTEND
echo ""
echo -e "${BLUE}[2/6] Fazendo build do frontend...${NC}"
cd $PROJECT_DIR/frontend
npm run build
echo -e "${GREEN}  ✓ Frontend buildado${NC}"

# 3. COPIAR BUILD PARA BACKEND
echo ""
echo -e "${BLUE}[3/6] Copiando build para backend...${NC}"
rm -rf $PROJECT_DIR/backend/staticfiles/frontend
mkdir -p $PROJECT_DIR/backend/staticfiles
cp -r dist $PROJECT_DIR/backend/staticfiles/frontend
echo -e "${GREEN}  ✓ Build copiado${NC}"

# 4. CONFIGURAR DJANGO URLS
echo ""
echo -e "${BLUE}[4/6] Configurando URLs do Django...${NC}"

cat > $PROJECT_DIR/backend/config/frontend_urls.py << 'EOF'
from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('login', TemplateView.as_view(template_name='index.html')),
    path('cargosnap', TemplateView.as_view(template_name='index.html')),
    path('cargosnap/<path:path>', TemplateView.as_view(template_name='index.html')),
]
EOF

echo -e "${GREEN}  ✓ URLs configuradas${NC}"

# 5. ATUALIZAR SETTINGS.PY
echo ""
echo -e "${BLUE}[5/6] Atualizando settings.py...${NC}"

# Adicionar configuração de templates e static
python3 << 'PYTHON_SCRIPT'
import re

settings_file = "/home/lfragoso/projetos/CargoSnap-ICTSI/backend/config/settings.py"

with open(settings_file, 'r') as f:
    content = f.read()

# Atualizar TEMPLATES
if "'DIRS': []" in content:
    content = content.replace(
        "'DIRS': []",
        "'DIRS': [BASE_DIR / 'staticfiles' / 'frontend']"
    )

# Garantir STATICFILES_DIRS
if "STATICFILES_DIRS" not in content:
    static_config = """
# Frontend build files
STATICFILES_DIRS = [
    BASE_DIR / 'staticfiles' / 'frontend' / 'assets',
]
"""
    # Adicionar antes de STATIC_URL
    content = content.replace("STATIC_URL = ", static_config + "\nSTATIC_URL = ")

with open(settings_file, 'w') as f:
    f.write(content)

print("Settings atualizado")
PYTHON_SCRIPT

echo -e "${GREEN}  ✓ Settings atualizado${NC}"

# 6. ATUALIZAR URLS PRINCIPAL
echo ""
echo -e "${BLUE}[6/6] Atualizando urls.py principal...${NC}"

python3 << 'PYTHON_SCRIPT'
import re

urls_file = "/home/lfragoso/projetos/CargoSnap-ICTSI/backend/config/urls.py"

with open(urls_file, 'r') as f:
    content = f.read()

# Adicionar import se não existir
if "from django.urls import path, include, re_path" not in content:
    content = content.replace(
        "from django.urls import path, include",
        "from django.urls import path, include, re_path"
    )

# Adicionar frontend URLs no final dos urlpatterns
if "include('config.frontend_urls')" not in content:
    # Encontrar o final de urlpatterns
    content = content.replace(
        "urlpatterns = [",
        """urlpatterns = [
    # API routes (devem vir ANTES das rotas do frontend)"""
    )
    
    # Adicionar frontend no final
    content = content.replace(
        "]",
        """    
    # Frontend (deve ser o ÚLTIMO para catch-all)
    re_path(r'^', include('config.frontend_urls')),
]""",
        1  # Substituir apenas a primeira ocorrência
    )

with open(urls_file, 'w') as f:
    f.write(content)

print("URLs atualizado")
PYTHON_SCRIPT

echo -e "${GREEN}  ✓ URLs atualizado${NC}"

# REMOVER SERVIÇO DO FRONTEND
echo ""
echo -e "${BLUE}Removendo serviço do frontend...${NC}"
sudo rm -f /etc/systemd/system/cargosnap-frontend.service
sudo systemctl daemon-reload
echo -e "${GREEN}  ✓ Serviço do frontend removido${NC}"

# REINICIAR BACKEND
echo ""
echo -e "${BLUE}Reiniciando backend...${NC}"
sudo systemctl restart cargosnap-backend
sleep 3
echo -e "${GREEN}  ✓ Backend reiniciado${NC}"

echo ""
echo -e "${CYAN}=============================================================${NC}"
echo -e "${GREEN}  ✓ CONFIGURAÇÃO CONCLUÍDA!${NC}"
echo -e "${CYAN}=============================================================${NC}"
echo ""
echo -e "${YELLOW}🌐 TUDO RODANDO NA PORTA 8501:${NC}"
echo -e "  ${CYAN}http://192.168.0.45:8501${NC}"
echo ""
echo -e "${YELLOW}Serviços ativos:${NC}"
echo -e "  ✓ Backend Django: porta 8501"
echo -e "  ✓ Frontend React (build): servido pelo Django na 8501"
echo ""
echo -e "${YELLOW}Comandos:${NC}"
echo -e "  ${CYAN}sudo systemctl status cargosnap-backend${NC}"
echo -e "  ${CYAN}sudo journalctl -u cargosnap-backend -f${NC}"
echo ""
echo -e "${CYAN}=============================================================${NC}"
