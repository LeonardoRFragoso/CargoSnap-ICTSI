# CargoSnap ICTSI - Frontend

Frontend da aplicação CargoSnap ICTSI construído com React, Vite e TailwindCSS.

## 🚀 Tecnologias

- **React 18+** - Biblioteca para construção de interfaces
- **Vite** - Build tool e dev server
- **React Router** - Navegação
- **TailwindCSS** - Framework CSS
- **Zustand** - Gerenciamento de estado
- **React Query** - Gerenciamento de dados assíncronos
- **Axios** - Cliente HTTP
- **Lucide React** - Ícones

## 📋 Pré-requisitos

- Node.js 18+ 
- npm ou yarn

## 🔧 Instalação

1. Instale as dependências:
```bash
npm install
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

3. Edite o arquivo `.env` com as configurações corretas:
```env
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=CargoSnap ICTSI
```

## 🏃 Executando o Projeto

### Modo de Desenvolvimento
```bash
npm run dev
```
Acesse: http://localhost:5173

### Build para Produção
```bash
npm run build
```

### Preview do Build
```bash
npm run preview
```

## 📁 Estrutura de Pastas

```
frontend/
├── public/              # Arquivos estáticos
├── src/
│   ├── components/      # Componentes reutilizáveis
│   │   └── layout/      # Componentes de layout
│   ├── pages/          # Páginas da aplicação
│   │   ├── auth/       # Páginas de autenticação
│   │   └── inspections/# Páginas de inspeções
│   ├── services/       # Serviços de API
│   ├── store/          # Estado global (Zustand)
│   ├── utils/          # Utilitários
│   ├── App.jsx         # Componente raiz
│   ├── main.jsx        # Ponto de entrada
│   └── index.css       # Estilos globais
├── .env.example        # Exemplo de variáveis de ambiente
├── package.json        # Dependências
├── vite.config.js      # Configuração do Vite
└── tailwind.config.js  # Configuração do Tailwind

```

## 🎨 Customização de Cores por Empresa

O projeto suporta 3 empresas com esquemas de cores personalizados:

### ICTSI
- Primary: `#0066CC` (Azul)
- Secondary: `#004080`

### iTracker
- Primary: `#00AA4A` (Verde)
- Secondary: `#008037`

### CLIA
- Primary: `#FF6600` (Laranja)
- Secondary: `#CC5200`

As cores estão configuradas no `tailwind.config.js` e podem ser usadas com:
```jsx
className="bg-ictsi-primary"
className="bg-itracker-primary"
className="bg-clia-primary"
```

## 📱 Mobile-First

O projeto foi desenvolvido com foco em dispositivos móveis:

- Design responsivo usando TailwindCSS
- Breakpoints otimizados para mobile, tablet e desktop
- Touch targets mínimos de 44x44px
- Safe areas para dispositivos com notch
- Sidebar responsiva com overlay em mobile

## 🔐 Autenticação

A autenticação é feita via JWT tokens:

1. Login retorna `access` e `refresh` tokens
2. Tokens são armazenados no Zustand com persistência
3. Refresh automático quando access token expira
4. Logout limpa todos os dados de autenticação

## 🛣️ Rotas

- `/login` - Página de login
- `/` - Dashboard (protegida)
- `/inspections` - Lista de inspeções (protegida)
- `/inspections/:id` - Detalhes da inspeção (protegida)
- `/inspections/new` - Nova inspeção (protegida)
- `/profile` - Perfil do usuário (protegida)

## 🔌 Integração com Backend

O frontend se comunica com o backend Django através da API REST:

- **Base URL**: Configurada em `VITE_API_URL`
- **Autenticação**: Bearer token no header
- **Refresh automático**: Interceptor do Axios
- **Proxy**: Configurado no Vite para desenvolvimento

## 📦 Scripts Disponíveis

- `npm run dev` - Inicia servidor de desenvolvimento
- `npm run build` - Gera build de produção
- `npm run preview` - Preview do build
- `npm run lint` - Verifica erros de código

## 🧪 Próximos Passos

- [ ] Implementar testes com Vitest
- [ ] Adicionar componentes shadcn/ui
- [ ] Implementar funcionalidades de inspeção
- [ ] Adicionar upload de imagens
- [ ] Implementar geração de relatórios
- [ ] Adicionar PWA support
- [ ] Implementar notificações push

## 📝 Notas

- Os warnings de CSS relacionados a `@tailwind` e `@apply` são esperados e serão processados corretamente pelo PostCSS
- O projeto usa persistência de estado com localStorage
- Configurado para funcionar com safe areas (iOS notch)
