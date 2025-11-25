# 🔧 Serviços Systemd - CargoSnap ICTSI

## 📦 Instalação dos Serviços

### **1️⃣ Executar Instalação (Uma vez)**

```bash
cd ~/projetos/CargoSnap-ICTSI

# Tornar script executável
chmod +x install-services.sh

# Executar instalação
./install-services.sh
```

Este script vai:
- ✅ Parar processos existentes
- ✅ Configurar variáveis de ambiente
- ✅ Instalar serviços no systemd
- ✅ Habilitar inicialização automática
- ✅ Iniciar os serviços

---

## 🎯 Comandos Principais

### **Ver Status**
```bash
# Status do backend
sudo systemctl status cargosnap-backend

# Status do frontend
sudo systemctl status cargosnap-frontend

# Status de ambos (resumido)
sudo systemctl status cargosnap-*
```

### **Iniciar Serviços**
```bash
# Iniciar backend
sudo systemctl start cargosnap-backend

# Iniciar frontend
sudo systemctl start cargosnap-frontend

# Iniciar ambos
sudo systemctl start cargosnap-backend cargosnap-frontend
```

### **Parar Serviços**
```bash
# Parar backend
sudo systemctl stop cargosnap-backend

# Parar frontend
sudo systemctl stop cargosnap-frontend

# Parar ambos
sudo systemctl stop cargosnap-backend cargosnap-frontend
```

### **Reiniciar Serviços**
```bash
# Reiniciar backend (após mudanças no código)
sudo systemctl restart cargosnap-backend

# Reiniciar frontend
sudo systemctl restart cargosnap-frontend

# Reiniciar ambos
sudo systemctl restart cargosnap-backend cargosnap-frontend
```

---

## 📊 Logs e Monitoramento

### **Ver Logs em Tempo Real**
```bash
# Logs do backend
sudo journalctl -u cargosnap-backend -f

# Logs do frontend
sudo journalctl -u cargosnap-frontend -f

# Logs de ambos
sudo journalctl -u cargosnap-backend -u cargosnap-frontend -f
```

### **Ver Logs Salvos**
```bash
# Backend
tail -f ~/projetos/CargoSnap-ICTSI/backend/logs/django.log

# Frontend
tail -f ~/projetos/CargoSnap-ICTSI/backend/logs/vite.log
```

### **Ver Últimas 100 Linhas**
```bash
# Backend
sudo journalctl -u cargosnap-backend -n 100

# Frontend
sudo journalctl -u cargosnap-frontend -n 100
```

### **Ver Logs de Hoje**
```bash
sudo journalctl -u cargosnap-backend --since today
sudo journalctl -u cargosnap-frontend --since today
```

---

## ⚙️ Configuração Automática

### **Habilitar Inicialização Automática (já configurado)**
```bash
sudo systemctl enable cargosnap-backend
sudo systemctl enable cargosnap-frontend
```

### **Desabilitar Inicialização Automática**
```bash
sudo systemctl disable cargosnap-backend
sudo systemctl disable cargosnap-frontend
```

### **Verificar se Está Habilitado**
```bash
systemctl is-enabled cargosnap-backend
systemctl is-enabled cargosnap-frontend
```

---

## 🔄 Após Atualizar Código

### **Backend (Python/Django)**
```bash
cd ~/projetos/CargoSnap-ICTSI

# 1. Fazer git pull
git pull

# 2. Ativar ambiente virtual e instalar dependências
cd backend
source venv/bin/activate
pip install -r requirements.txt

# 3. Executar migrações
python manage.py migrate

# 4. Coletar arquivos estáticos (se necessário)
python manage.py collectstatic --noinput

# 5. Reiniciar serviço
deactivate
sudo systemctl restart cargosnap-backend

# 6. Verificar status
sudo systemctl status cargosnap-backend
```

### **Frontend (React)**
```bash
cd ~/projetos/CargoSnap-ICTSI

# 1. Fazer git pull
git pull

# 2. Instalar dependências (se houver novas)
cd frontend
npm install

# 3. Reiniciar serviço
sudo systemctl restart cargosnap-frontend

# 4. Verificar status
sudo systemctl status cargosnap-frontend
```

---

## 🛠️ Manutenção

### **Recarregar Configuração dos Serviços**
```bash
# Após editar arquivos .service
sudo systemctl daemon-reload
sudo systemctl restart cargosnap-backend cargosnap-frontend
```

### **Editar Configuração do Serviço**
```bash
# Editar backend
sudo nano /etc/systemd/system/cargosnap-backend.service

# Editar frontend
sudo nano /etc/systemd/system/cargosnap-frontend.service

# Depois de editar:
sudo systemctl daemon-reload
sudo systemctl restart cargosnap-backend cargosnap-frontend
```

### **Verificar Configuração**
```bash
# Ver configuração completa
systemctl cat cargosnap-backend
systemctl cat cargosnap-frontend
```

---

## 🐛 Troubleshooting

### **Serviço Não Inicia**
```bash
# Ver motivo da falha
sudo systemctl status cargosnap-backend
sudo journalctl -u cargosnap-backend -n 50

# Testar manualmente
cd ~/projetos/CargoSnap-ICTSI/backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8501
```

### **Porta em Uso**
```bash
# Ver o que está usando a porta
sudo lsof -i:8501
sudo lsof -i:3000

# Matar processo
sudo kill -9 PID_AQUI
```

### **Reiniciar Tudo**
```bash
# Parar serviços
sudo systemctl stop cargosnap-backend cargosnap-frontend

# Matar processos remanescentes
sudo lsof -ti:8501 | xargs sudo kill -9
sudo lsof -ti:3000 | xargs sudo kill -9

# Iniciar novamente
sudo systemctl start cargosnap-backend cargosnap-frontend
```

---

## 🗑️ Desinstalar Serviços

```bash
# 1. Parar e desabilitar
sudo systemctl stop cargosnap-backend cargosnap-frontend
sudo systemctl disable cargosnap-backend cargosnap-frontend

# 2. Remover arquivos
sudo rm /etc/systemd/system/cargosnap-backend.service
sudo rm /etc/systemd/system/cargosnap-frontend.service

# 3. Recarregar systemd
sudo systemctl daemon-reload
sudo systemctl reset-failed
```

---

## 📋 Checklist de Verificação

### **Serviços Rodando?**
- [ ] `sudo systemctl status cargosnap-backend` mostra "active (running)"
- [ ] `sudo systemctl status cargosnap-frontend` mostra "active (running)"

### **URLs Acessíveis?**
- [ ] http://192.168.0.45:8501 - Backend API
- [ ] http://192.168.0.45:3000 - Frontend
- [ ] http://192.168.0.45:8501/admin - Django Admin

### **Inicialização Automática?**
- [ ] `systemctl is-enabled cargosnap-backend` retorna "enabled"
- [ ] `systemctl is-enabled cargosnap-frontend` retorna "enabled"

### **Logs Sem Erros?**
- [ ] `sudo journalctl -u cargosnap-backend -n 20` sem erros críticos
- [ ] `sudo journalctl -u cargosnap-frontend -n 20` sem erros críticos

---

## 🌐 URLs de Acesso

**Na mesma rede:**
- Frontend: `http://192.168.0.45:3000`
- Backend API: `http://192.168.0.45:8501/api`
- Django Admin: `http://192.168.0.45:8501/admin`

**Na própria VM:**
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8501`

---

## 📝 Arquivos de Configuração

| Arquivo | Localização | Descrição |
|---------|-------------|-----------|
| Backend Service | `/etc/systemd/system/cargosnap-backend.service` | Configuração systemd backend |
| Frontend Service | `/etc/systemd/system/cargosnap-frontend.service` | Configuração systemd frontend |
| Environment | `~/projetos/CargoSnap-ICTSI/backend/.env` | Variáveis de ambiente |
| Logs Backend | `~/projetos/CargoSnap-ICTSI/backend/logs/django.log` | Logs Django |
| Logs Frontend | `~/projetos/CargoSnap-ICTSI/backend/logs/vite.log` | Logs Vite |

---

## ✅ Vantagens dos Serviços Systemd

- ✅ Inicialização automática no boot
- ✅ Reinicialização automática em caso de crash
- ✅ Logs centralizados via journalctl
- ✅ Gestão profissional de processos
- ✅ Integração com firewall e SELinux
- ✅ Controle de recursos (CPU, memória)
- ✅ Ordem de inicialização (frontend após backend)

---

**Pronto! Serviços configurados profissionalmente! 🚀**
