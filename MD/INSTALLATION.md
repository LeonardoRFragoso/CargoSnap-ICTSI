# Guia de Instalação - CargoSnap ICTSI

Este guia fornece instruções passo a passo para configurar e executar o projeto CargoSnap ICTSI.

## 📋 Pré-requisitos

### Backend
- Python 3.11+
- PostgreSQL 14+
- pip (gerenciador de pacotes Python)

### Frontend
- Node.js 18+
- npm ou yarn

## 🚀 Instalação do Backend (Django)

### 1. Navegue até o diretório do backend
```bash
cd backend
```

### 2. Crie um ambiente virtual Python
```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instale as dependências
```bash
pip install -r requirements.txt
```

### 5. Configure as variáveis de ambiente

Copie o arquivo de exemplo e edite com suas configurações:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:
```env
# Django Settings
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=cargosnap_db
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
```

### 6. Crie o banco de dados PostgreSQL

Acesse o PostgreSQL e execute:
```sql
CREATE DATABASE cargosnap_db;
CREATE USER postgres WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE cargosnap_db TO postgres;
```

### 7. Execute as migrações
```bash
python manage.py migrate
```

### 8. Crie as empresas iniciais
```bash
python manage.py create_companies
```

### 9. Crie um superusuário (admin)
```bash
python manage.py createsuperuser
```

Siga as instruções e forneça:
- Username
- Email
- Password
- Company (escolha uma das 3: ICTSI, iTracker ou CLIA)

### 10. Execute o servidor de desenvolvimento
```bash
python manage.py runserver
```

O backend estará disponível em: http://localhost:8000

**Acesso ao Admin:** http://localhost:8000/admin

**Documentação da API:** http://localhost:8000/api/docs/

## 🎨 Instalação do Frontend (React)

### 1. Navegue até o diretório do frontend
```bash
cd frontend
```

### 2. Instale as dependências
```bash
npm install
```

### 3. Configure as variáveis de ambiente

Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

Edite o arquivo `.env` se necessário (valores padrão já estão corretos):
```env
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=CargoSnap ICTSI
```

### 4. Execute o servidor de desenvolvimento
```bash
npm run dev
```

O frontend estará disponível em: http://localhost:5173

## ✅ Verificação da Instalação

1. **Backend funcionando:** Acesse http://localhost:8000/api/docs/ - você deve ver a documentação da API
2. **Frontend funcionando:** Acesse http://localhost:5173 - você deve ver a tela de login
3. **Login:** Use as credenciais do superusuário criado

## 🔧 Comandos Úteis

### Backend

```bash
# Criar novas migrações após modificar models
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos (produção)
python manage.py collectstatic

# Executar testes
python manage.py test

# Criar empresas iniciais
python manage.py create_companies
```

### Frontend

```bash
# Instalar dependências
npm install

# Executar em desenvolvimento
npm run dev

# Build para produção
npm run build

# Preview do build
npm run preview

# Lint
npm run lint
```

## 🐳 Docker (Opcional)

Para executar com Docker, será necessário criar os arquivos `Dockerfile` e `docker-compose.yml`.

## 🗄️ Estrutura do Banco de Dados

O comando `migrate` criará as seguintes tabelas principais:
- `core_company` - Empresas (ICTSI, iTracker, CLIA)
- `core_user` - Usuários do sistema
- `core_auditlog` - Logs de auditoria
- E outras tabelas padrão do Django

## 🔐 Usuários de Teste

Após criar as empresas e o superusuário, você pode criar usuários adicionais via:
1. Admin Django (http://localhost:8000/admin)
2. API REST (programaticamente)

## 📱 Testando no Mobile

Para testar em dispositivos móveis na mesma rede:

1. Descubra o IP local da sua máquina:
   - Windows: `ipconfig`
   - Linux/Mac: `ifconfig` ou `ip addr`

2. Adicione o IP ao `ALLOWED_HOSTS` no backend `.env`:
   ```env
   ALLOWED_HOSTS=localhost,127.0.0.1,192.168.x.x
   ```

3. Adicione o IP ao `CORS_ALLOWED_ORIGINS` no backend `.env`:
   ```env
   CORS_ALLOWED_ORIGINS=http://localhost:5173,http://192.168.x.x:5173
   ```

4. Acesse do dispositivo móvel: `http://192.168.x.x:5173`

## ❗ Problemas Comuns

### Erro de conexão com PostgreSQL
- Verifique se o PostgreSQL está rodando
- Verifique as credenciais no arquivo `.env`
- Verifique se o banco de dados foi criado

### Erro de CORS no frontend
- Verifique se o `CORS_ALLOWED_ORIGINS` no backend inclui a URL do frontend
- Verifique se o backend está rodando

### Erro "Module not found" no Python
- Certifique-se de que o ambiente virtual está ativado
- Execute `pip install -r requirements.txt` novamente

### Erro de dependências no npm
- Delete a pasta `node_modules` e `package-lock.json`
- Execute `npm install` novamente

## 📞 Suporte

Para problemas ou dúvidas, consulte:
- README principal do projeto
- Documentação da API (http://localhost:8000/api/docs/)
- README do frontend (frontend/README.md)
