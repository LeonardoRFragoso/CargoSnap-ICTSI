# 🚀 Deploy - VM Linux (itk-dev-02)

## 📋 Guia Rápido de Deploy

### 1️⃣ **Setup Inicial da VM** (Apenas uma vez)

```bash
# Na VM Linux
cd ~/projetos/CargoSnap-ICTSI

# Tornar scripts executáveis
chmod +x setup-vm.sh start-dev.sh stop-dev.sh

# Executar setup (instala dependências)
./setup-vm.sh
```

---

### 2️⃣ **Configurar Backend**

```bash
cd ~/projetos/CargoSnap-ICTSI/backend

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# Executar migrações
python manage.py migrate

# Criar superusuário (admin)
python manage.py createsuperuser

# Sair do ambiente virtual
deactivate
```

---

### 3️⃣ **Configurar Frontend**

```bash
cd ~/projetos/CargoSnap-ICTSI/frontend

# Usar configuração pré-configurada para VM (192.168.0.45:8501)
cp .env.vm .env

# Instalar dependências
npm install
```

**✅ O arquivo `.env.vm` já está configurado com:**
```bash
VITE_API_URL=http://192.168.0.45:8501/api
```

**⚠️ Se sua VM usar IP diferente de 192.168.0.45:**
```bash
# Editar .env manualmente
nano .env

# Ou criar do .env.example
cp .env.example .env
nano .env
```

**Altere para o IP correto:**
```bash
VITE_API_URL=http://SEU_IP_DA_VM:8501/api
```

---

### 4️⃣ **Iniciar Aplicação**

```bash
# Voltar para raiz do projeto
cd ~/projetos/CargoSnap-ICTSI

# Iniciar backend (porta 8501) e frontend (porta 3000)
./start-dev.sh
```

**Saída esperada:**
```
=============================================================
  ✓ Ambiente CargoSnap ICTSI iniciado!
=============================================================

📊 Serviços:
  Backend (Django):  http://localhost:8501
  Frontend (React): http://localhost:3000
  Admin Django:     http://localhost:8501/admin
  API Docs:         http://localhost:8501/api
```

---

### 5️⃣ **Acessar Aplicação**

**Do seu computador ou smartphone:**
- Frontend: `http://192.168.0.45:3000`
- Backend API: `http://192.168.0.45:8501/api`
- Django Admin: `http://192.168.0.45:8501/admin`

**⚠️ Certifique-se de estar na mesma rede da VM!**

---

### 6️⃣ **Parar Aplicação**

```bash
cd ~/projetos/CargoSnap-ICTSI
./stop-dev.sh
```

---

## 🔧 Comandos Úteis

### Ver Logs em Tempo Real

```bash
# Backend
tail -f ~/projetos/CargoSnap-ICTSI/backend/logs/django.log

# Frontend
tail -f ~/projetos/CargoSnap-ICTSI/backend/logs/vite.log
```

### Reiniciar Serviços

```bash
cd ~/projetos/CargoSnap-ICTSI
./stop-dev.sh
./start-dev.sh
```

### Verificar Processos

```bash
# Ver se backend está rodando
lsof -i:8501

# Ver se frontend está rodando
lsof -i:3000

# Ver todos os processos Python
ps aux | grep python

# Ver todos os processos Node
ps aux | grep node
```

### Sincronizar Dados CargoSnap

```bash
cd ~/projetos/CargoSnap-ICTSI/backend
source venv/bin/activate
python manage.py shell

# No shell Python:
from apps.cargosnap_integration.services import CargoSnapAPIService
service = CargoSnapAPIService()
sync_log = service.full_sync(download_images=True)
```

---

## 🔥 Troubleshooting

### Porta 8501 em uso

```bash
# Matar processo na porta 8501
lsof -ti:8501 | xargs kill -9

# Ou usar o script
./stop-dev.sh
```

### Erro de permissão nos scripts

```bash
chmod +x setup-vm.sh start-dev.sh stop-dev.sh
```

### Backend não inicia

```bash
# Ver logs
cat ~/projetos/CargoSnap-ICTSI/backend/logs/django.log

# Testar manualmente
cd ~/projetos/CargoSnap-ICTSI/backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8501
```

### Frontend não conecta ao backend

1. Verificar .env do frontend:
   ```bash
   cat ~/projetos/CargoSnap-ICTSI/frontend/.env
   ```

2. Verificar se o IP está correto

3. Verificar firewall:
   ```bash
   sudo ufw status
   sudo ufw allow 8501/tcp
   ```

### Erro de CORS

Edite `backend/config/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://SEU_IP:3000",
]
```

---

## 📦 Arquitetura

```
CargoSnap-ICTSI/
├── backend/                  # Django (porta 8501)
│   ├── venv/                # Ambiente virtual Python
│   ├── manage.py
│   ├── config/              # Settings
│   ├── apps/
│   │   ├── cargosnap_integration/
│   │   └── inspections/
│   └── logs/                # Logs (criado automaticamente)
│
├── frontend/                 # React + Vite (porta 3000)
│   ├── node_modules/
│   ├── src/
│   └── .env                 # CONFIGURAR!
│
├── start-dev.sh             # Iniciar aplicação
├── stop-dev.sh              # Parar aplicação
└── setup-vm.sh              # Setup inicial
```

---

## 🌐 Portas Utilizadas

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| Backend Django | 8501 | API REST + Admin |
| Frontend React | 3000 | Interface do usuário |
| PostgreSQL | 5432 | Banco de dados (opcional) |

---

## 🔐 Segurança

### Firewall (UFW)

```bash
# Ativar firewall
sudo ufw enable

# Permitir portas necessárias
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 8501/tcp  # Backend
sudo ufw allow 3000/tcp  # Frontend (dev)
sudo ufw allow 80/tcp    # HTTP (produção)
sudo ufw allow 443/tcp   # HTTPS (produção)

# Ver status
sudo ufw status
```

### Nginx (Produção - Opcional)

Para produção com Nginx:

```bash
# Instalar Nginx
sudo apt install nginx

# Copiar configuração
sudo nano /etc/nginx/sites-available/cargosnap
```

**Exemplo de configuração Nginx:**
```nginx
server {
    listen 80;
    server_name SEU_IP_OU_DOMINIO;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Django Admin
    location /admin {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📊 Monitoramento

### Verificar Status

```bash
# Backend
curl http://localhost:8501/api/

# Frontend
curl http://localhost:3000/

# Ver recursos
htop
```

### Logs

```bash
# Backend logs
tail -f ~/projetos/CargoSnap-ICTSI/backend/logs/django.log

# Frontend logs
tail -f ~/projetos/CargoSnap-ICTSI/backend/logs/vite.log

# System logs
journalctl -f
```

---

## 🎯 Checklist de Deploy

- [ ] Setup inicial executado (`./setup-vm.sh`)
- [ ] Ambiente virtual Python criado
- [ ] Dependências Python instaladas
- [ ] Migrações executadas
- [ ] Superusuário criado
- [ ] Frontend .env configurado com IP correto
- [ ] Dependências Node instaladas
- [ ] Firewall configurado
- [ ] Aplicação iniciada (`./start-dev.sh`)
- [ ] Acesso ao frontend funcionando
- [ ] Acesso ao backend funcionando
- [ ] Login no admin funcionando

---

## 📞 Comandos Rápidos

```bash
# Setup inicial (uma vez)
./setup-vm.sh

# Iniciar
./start-dev.sh

# Parar
./stop-dev.sh

# Ver logs
tail -f backend/logs/django.log
tail -f backend/logs/vite.log

# Reiniciar
./stop-dev.sh && ./start-dev.sh
```

---

## ✨ Pronto!

Sua aplicação CargoSnap ICTSI está rodando na VM Linux! 🎉

**URLs:**
- Frontend: `http://SEU_IP:3000`
- Backend: `http://SEU_IP:8501/admin`
