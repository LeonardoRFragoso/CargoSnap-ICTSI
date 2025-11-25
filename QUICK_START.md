# ⚡ Quick Start - Deploy VM Linux

## 🚀 Comandos Rápidos (Copy & Paste)

### 1️⃣ Preparar Scripts (Uma vez)

```bash
cd ~/projetos/CargoSnap-ICTSI
chmod +x setup-vm.sh start-dev.sh stop-dev.sh
```

### 2️⃣ Setup Inicial (Uma vez)

```bash
# Executar setup completo
./setup-vm.sh
```

### 3️⃣ Configurar Backend (Uma vez)

```bash
cd ~/projetos/CargoSnap-ICTSI/backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
deactivate
cd ..
```

### 4️⃣ Configurar Frontend (Uma vez)

```bash
cd ~/projetos/CargoSnap-ICTSI/frontend

# Opção 1: Usar configuração pré-configurada para VM (192.168.0.45:8501)
cp .env.vm .env

# Opção 2: Criar do zero
# cp .env.example .env
# nano .env  # E editar manualmente

npm install
cd ..
```

**✅ Arquivo `.env.vm` já está configurado com:**
```
VITE_API_URL=http://192.168.0.45:8501/api
```

**⚠️ Se precisar mudar o IP:** Edite `.env` manualmente:
```bash
nano ~/projetos/CargoSnap-ICTSI/frontend/.env
```

### 5️⃣ Iniciar Aplicação

```bash
cd ~/projetos/CargoSnap-ICTSI
./start-dev.sh
```

### 6️⃣ Parar Aplicação

```bash
cd ~/projetos/CargoSnap-ICTSI
./stop-dev.sh
```

---

## 📱 URLs de Acesso

**VM: 192.168.0.45**

- **Frontend:** `http://192.168.0.45:3000`
- **Backend API:** `http://192.168.0.45:8501/api`
- **Admin Django:** `http://192.168.0.45:8501/admin`

**⚠️ Acesse de qualquer dispositivo na mesma rede!**

---

## 🔍 Descobrir IP da VM

```bash
# Ver IP da VM
hostname -I | awk '{print $1}'

# Ou
ip addr show | grep "inet " | grep -v 127.0.0.1
```

---

## 📊 Verificar Status

```bash
# Ver se está rodando
lsof -i:8501  # Backend
lsof -i:3000  # Frontend

# Ver logs
tail -f ~/projetos/CargoSnap-ICTSI/backend/logs/django.log
tail -f ~/projetos/CargoSnap-ICTSI/backend/logs/vite.log
```

---

## 🔥 Solução Rápida de Problemas

### Porta em uso:
```bash
./stop-dev.sh
```

### Reiniciar tudo:
```bash
./stop-dev.sh && ./start-dev.sh
```

### Liberar portas manualmente:
```bash
lsof -ti:8501 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

---

## ✅ Checklist Rápido

```bash
# 1. Scripts executáveis?
ls -la *.sh

# 2. Backend configurado?
ls ~/projetos/CargoSnap-ICTSI/backend/venv

# 3. Frontend configurado?
ls ~/projetos/CargoSnap-ICTSI/frontend/node_modules
cat ~/projetos/CargoSnap-ICTSI/frontend/.env

# 4. Aplicação rodando?
lsof -i:8501
lsof -i:3000

# 5. Acessível externamente?
curl http://localhost:8501/api/
```

---

## 🎯 Tudo em Um Comando (Primeira vez)

```bash
cd ~/projetos/CargoSnap-ICTSI && \
chmod +x *.sh && \
cd backend && \
python3 -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt && \
python manage.py migrate && \
deactivate && \
cd ../frontend && \
npm install && \
cd .. && \
echo "✅ Setup completo! Agora configure o .env e execute ./start-dev.sh"
```

**Depois configure o .env:**
```bash
nano ~/projetos/CargoSnap-ICTSI/frontend/.env
```

**E inicie:**
```bash
cd ~/projetos/CargoSnap-ICTSI
./start-dev.sh
```

---

## 🚀 Pronto para Usar!

**Acesse do seu computador ou smartphone:**
- `http://192.168.0.45:3000`

**Login Admin:**
- `http://192.168.0.45:8501/admin`
