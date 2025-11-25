# 🎨 Guia de Templates - CargoSnap ICTSI

## ✅ Templates Criados

### 1. **Base Template** (`templates/base.html`)
- Layout principal com navbar, footer e Bootstrap 5
- Menu de navegação para usuários autenticados
- Sistema de mensagens (alerts)
- Responsivo e moderno

### 2. **Autenticação** (`templates/auth/`)
- ✅ **login.html** - Tela de login com design moderno
- ✅ **register.html** - Registro de novos usuários
- ✅ **password_reset.html** - Recuperação de senha
- ✅ **password_reset_done.html** - Confirmação de envio

### 3. **Dashboard** (`templates/dashboard/`)
- ✅ **index.html** - Dashboard com:
  - Cards de estatísticas (inspeções, ocorrências)
  - Gráficos com Chart.js
  - Tabela de inspeções recentes
  - Design moderno e responsivo

---

## 🚀 Como Acessar

### 1. Inicie o servidor (se não estiver rodando)
```powershell
cd backend
python manage.py runserver
```

### 2. Acesse as páginas

#### 🔐 **Login**
```
http://127.0.0.1:8000/login/
ou
http://127.0.0.1:8000/
```

**Credenciais:**
- Usuário: `Leonardo`
- Senha: [a que você digitou]

#### 📝 **Registro**
```
http://127.0.0.1:8000/register/
```
- Crie novos usuários
- Escolha entre 3 empresas (ICTSI, iTracker, CLIA)

#### 📊 **Dashboard**
```
http://127.0.0.1:8000/dashboard/
```
- Acesso após login
- Mostra estatísticas em tempo real
- Gráficos interativos
- Inspeções recentes

#### 🔑 **Recuperar Senha**
```
http://127.0.0.1:8000/password-reset/
```

---

## 🎨 Características dos Templates

### Design
- ✅ **Bootstrap 5** - Framework CSS moderno
- ✅ **Bootstrap Icons** - Ícones profissionais
- ✅ **Gradientes** - Backgrounds modernos
- ✅ **Responsivo** - Funciona em mobile/tablet/desktop
- ✅ **Chart.js** - Gráficos interativos no dashboard

### Funcionalidades
- ✅ **Sistema de mensagens** - Feedback visual
- ✅ **Validação de formulários** - Django + Bootstrap
- ✅ **Multi-tenancy** - Escolha de empresa no registro
- ✅ **Navbar dinâmica** - Mostra nome do usuário e empresa
- ✅ **Dropdown de perfil** - Acesso rápido a configurações

---

## 📁 Estrutura de Arquivos

```
backend/
├── templates/
│   ├── base.html                    # Template base
│   ├── auth/
│   │   ├── login.html              # Login
│   │   ├── register.html           # Registro
│   │   ├── password_reset.html     # Recuperar senha
│   │   └── password_reset_done.html # Confirmação
│   └── dashboard/
│       └── index.html              # Dashboard principal
│
└── apps/core/
    ├── forms.py                    # Formulários (LoginForm, RegisterForm)
    └── views.py                    # Views (login_view, dashboard_view)
```

---

## 🔧 URLs Configuradas

| URL | View | Template | Descrição |
|-----|------|----------|-----------|
| `/` | `login_view` | `auth/login.html` | Página inicial (login) |
| `/login/` | `login_view` | `auth/login.html` | Tela de login |
| `/register/` | `register_view` | `auth/register.html` | Registro de usuário |
| `/logout/` | `logout_view` | - | Logout (redirect para login) |
| `/dashboard/` | `dashboard_view` | `dashboard/index.html` | Dashboard principal |
| `/password-reset/` | `password_reset_view` | `auth/password_reset.html` | Recuperar senha |
| `/password-reset/done/` | `password_reset_done_view` | `auth/password_reset_done.html` | Confirmação |

---

## 💡 Próximas Melhorias Sugeridas

### Templates Adicionais
- [ ] Página de perfil do usuário
- [ ] Lista de inspeções (CRUD completo)
- [ ] Formulário de nova inspeção
- [ ] Lista de ocorrências (Issues)
- [ ] Relatórios (visualização e download)
- [ ] Configurações da conta

### Funcionalidades
- [ ] Envio real de email (recuperação de senha)
- [ ] Upload de avatar do usuário
- [ ] Filtros avançados no dashboard
- [ ] Exportar dados para Excel/PDF
- [ ] Notificações em tempo real (WebSocket)

---

## 🎯 Como Testar

### 1. Fazer Login
1. Acesse `http://127.0.0.1:8000/`
2. Digite: `Leonardo` / `[sua senha]`
3. Clique em "Entrar"
4. Você será redirecionado para o dashboard

### 2. Criar Novo Usuário
1. Acesse `http://127.0.0.1:8000/register/`
2. Preencha todos os campos
3. Escolha uma empresa (ICTSI, iTracker ou CLIA)
4. Clique em "Criar Conta"
5. Faça login com o novo usuário

### 3. Explorar Dashboard
1. Veja as estatísticas (cards coloridos)
2. Navegue pelos gráficos
3. Verifique a tabela de inspeções
4. Teste o dropdown do perfil

### 4. Logout
1. Clique no seu nome (canto superior direito)
2. Clique em "Sair"
3. Você será redirecionado para login

---

## 🐛 Notas sobre Erros de Lint

Você pode ver erros de lint no arquivo `dashboard/index.html` relacionados ao JavaScript.

**Isso é NORMAL e não afeta o funcionamento!**

Motivo: O editor tenta validar Django Template Language (`{{ }}`) como JavaScript puro, mas quando o Django renderiza o template, ele substitui essas variáveis pelos valores corretos.

---

## 📞 Suporte

- **Documentação Django**: https://docs.djangoproject.com/
- **Bootstrap 5**: https://getbootstrap.com/docs/5.3/
- **Chart.js**: https://www.chartjs.org/docs/

---

**🎉 Templates 100% Funcionais e Prontos para Uso!**
