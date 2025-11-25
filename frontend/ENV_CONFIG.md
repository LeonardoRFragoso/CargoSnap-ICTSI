# 🔧 Configuração do Ambiente (.env)

## 📋 Arquivos Disponíveis

### `.env.example`
Template padrão com configuração local (localhost:8000)

### `.env.vm` ✅ **RECOMENDADO PARA VM**
Configuração pré-configurada para VM de desenvolvimento:
- **IP:** 192.168.0.45
- **Porta:** 8501

### `.env`
Arquivo ativo (não versionado no Git)

---

## 🚀 Setup Rápido

### **Para VM (192.168.0.45:8501):**
```bash
cp .env.vm .env
```

### **Para Local (localhost:8000):**
```bash
cp .env.example .env
```

### **Para Customizar:**
```bash
cp .env.example .env
nano .env  # Editar manualmente
```

---

## 📝 Variáveis Disponíveis

```bash
# URL da API Backend
VITE_API_URL=http://192.168.0.45:8501/api

# Nome da Aplicação
VITE_APP_NAME=CargoSnap ICTSI

# Versão
VITE_APP_VERSION=1.0.0

# Features
VITE_ENABLE_PWA=true
VITE_ENABLE_OFFLINE_MODE=false
```

---

## 🌐 Configurações por Ambiente

### **Desenvolvimento Local (Windows/Linux)**
```bash
VITE_API_URL=http://localhost:8000/api
```

### **VM de Desenvolvimento (itk-dev-02)**
```bash
VITE_API_URL=http://192.168.0.45:8501/api
```

### **Produção**
```bash
VITE_API_URL=https://seu-dominio.com/api
```

---

## ⚠️ IMPORTANTE

1. **Nunca commit o arquivo `.env`** - Está no .gitignore
2. **Use `.env.vm` na VM** - Já está configurado
3. **Reinicie o frontend após alterar .env** - `npm run dev`

---

## 🔍 Verificar Configuração Atual

```bash
# Ver conteúdo do .env
cat .env

# Testar conexão com API
curl http://192.168.0.45:8501/api/
```

---

## 🐛 Troubleshooting

### Frontend não conecta ao backend:

1. Verificar .env:
   ```bash
   cat .env
   ```

2. Verificar se backend está rodando:
   ```bash
   curl http://192.168.0.45:8501/api/
   ```

3. Verificar rede:
   ```bash
   ping 192.168.0.45
   ```

4. Reiniciar frontend:
   ```bash
   # Parar (Ctrl+C)
   npm run dev
   ```

---

## 📱 Acesso Mobile

Para acessar do smartphone, use o mesmo IP:
```
http://192.168.0.45:3000
```

**Requisitos:**
- Smartphone na mesma rede Wi-Fi
- Firewall liberado na VM (portas 3000 e 8501)

---

## ✅ Checklist

- [ ] Arquivo `.env` existe?
- [ ] `VITE_API_URL` aponta para IP correto?
- [ ] Backend está rodando na porta 8501?
- [ ] Frontend reiniciado após alterar .env?
- [ ] Mesma rede (smartphone/computador/VM)?
