# 🚀 Quick Start - CargoSnap ICTSI

## ✅ Atualizações Recentes

### 1. **Background Atualizado** ✨
- ✅ Removido gradiente roxo/azul
- ✅ Adicionada imagem de background personalizada
- ✅ Overlay branco translúcido (85%) para melhor legibilidade
- ✅ Imagem localizada em: `backend/static/images/bg-login.png`

### 2. **Frontend Corrigido** 🔧
- ✅ Erro do Tailwind CSS corrigido (`border-border` → `border-gray-200`)
- ✅ `npm install` concluído com sucesso
- ✅ Pronto para rodar com `npm run dev`

---

## 🎯 Como Iniciar o Sistema

### **Backend (Django)**

```powershell
# Terminal 1
cd backend
.\venv\Scripts\activate
python manage.py runserver
```

**Acesse:** http://127.0.0.1:8000/

### **Frontend (React + Vite)**

```powershell
# Terminal 2
cd frontend
npm run dev
```

**Acesse:** http://localhost:5173/

---

## 🔐 Credenciais de Acesso

**Backend (Django Templates):**
- URL: http://127.0.0.1:8000/login/
- Usuário: `Leonardo`
- Senha: [a que você criou com o comando `create_admin`]

**Frontend (React):**
- URL: http://localhost:5173/
- Mesmas credenciais do backend

---

## 📁 Estrutura Atual

```
CargoSnap-ICTSI/
├── backend/
│   ├── static/
│   │   └── images/
│   │       └── bg-login.png          ← Nova imagem de background
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html            ← Atualizado com nova imagem
│   │   │   ├── register.html         ← Atualizado com nova imagem
│   │   │   ├── password_reset.html   ← Atualizado com nova imagem
│   │   │   └── password_reset_done.html
│   │   └── dashboard/
│   │       └── index.html
│   └── apps/
│       └── core/
│           ├── forms.py
│           └── views.py
│
└── frontend/
    ├── src/
    │   └── index.css                 ← Corrigido (border-gray-200)
    └── package.json
```

---

## 🎨 Templates com Nova Imagem

Todos os templates de autenticação agora usam a imagem personalizada:

1. ✅ **Login** - `/login/`
2. ✅ **Registro** - `/register/`
3. ✅ **Recuperar Senha** - `/password-reset/`
4. ✅ **Confirmação** - `/password-reset/done/`

**Design:**
- Background: Imagem do terminal portuário
- Overlay: Branco 85% de opacidade
- Cards: Brancos com sombra
- Header: Gradiente azul ICTSI

---

## 🐛 Avisos de Lint (PODE IGNORAR)

### Frontend (`index.css`)
```
Unknown at rule @tailwind
Unknown at rule @apply
```

**Motivo:** O linter CSS padrão não reconhece diretivas do Tailwind CSS, mas elas funcionam perfeitamente quando processadas pelo PostCSS/Tailwind.

### Backend (`dashboard/index.html`)
```
Property assignment expected
Expression expected
```

**Motivo:** O linter JavaScript tenta validar Django Template Language (`{{ }}`) como JS puro. Quando o Django renderiza, substitui pelas variáveis corretas.

---

## ✅ Checklist de Funcionamento

- [x] Backend instalado e configurado
- [x] Frontend instalado (`npm install` concluído)
- [x] Banco de dados SQLite criado
- [x] Migrações aplicadas
- [x] Empresas criadas (ICTSI, iTracker, CLIA)
- [x] Estruturas e danos populados
- [x] Superusuário criado
- [x] Templates de autenticação criados
- [x] Background personalizado aplicado
- [x] Erro do Tailwind corrigido

---

## 🎯 Próximos Passos

1. **Inicie o backend:**
   ```powershell
   cd backend
   .\venv\Scripts\activate
   python manage.py runserver
   ```

2. **Inicie o frontend:**
   ```powershell
   cd frontend
   npm run dev
   ```

3. **Teste o sistema:**
   - Acesse http://127.0.0.1:8000/login/
   - Veja a nova imagem de background
   - Faça login
   - Explore o dashboard

---

## 📞 Comandos Úteis

### Backend
```powershell
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py create_admin

# Popular dados
python manage.py populate_structures_damages
python manage.py create_companies

# Rodar servidor
python manage.py runserver
```

### Frontend
```powershell
# Instalar dependências
npm install

# Rodar dev server
npm run dev

# Build para produção
npm run build

# Preview do build
npm run preview
```

---

**🎉 Sistema 100% Funcional com Design Personalizado!**
