# 🎨 Design System - CargoSnap ICTSI

## 📐 Guia de Estilo e Componentes Padrão

Este documento define os padrões visuais e componentes reutilizáveis do sistema.

---

## 🎯 Princípios de Design

1. **Consistência** - Mesmos padrões em todas as páginas
2. **Clareza** - Interface limpa e fácil de entender
3. **Feedback** - Respostas visuais claras para ações do usuário
4. **Acessibilidade** - Cores com bom contraste e textos legíveis
5. **Responsividade** - Funciona bem em todos os tamanhos de tela

---

## 🎨 Paleta de Cores

### Cores Principais
```css
/* Primary - Azul */
--blue-50: #eff6ff
--blue-100: #dbeafe
--blue-500: #3b82f6
--blue-600: #2563eb  /* Principal */
--blue-700: #1d4ed8
--blue-800: #1e40af

/* Secondary - Cinza */
--gray-50: #f9fafb   /* Background */
--gray-100: #f3f4f6
--gray-300: #d1d5db  /* Borders */
--gray-500: #6b7280
--gray-600: #4b5563
--gray-700: #374151
--gray-900: #111827  /* Text */

/* Success - Verde */
--green-600: #16a34a
--green-700: #15803d

/* Warning - Amarelo */
--yellow-500: #eab308
--yellow-600: #ca8a04

/* Danger - Vermelho */
--red-600: #dc2626
--red-700: #b91c1c
```

### Uso das Cores
- **Azul**: Ações primárias, links, destaques
- **Verde**: Sucesso, confirmações, status positivo
- **Amarelo**: Avisos, pendências
- **Vermelho**: Erros, exclusões, alertas críticos
- **Cinza**: Texto, bordas, backgrounds neutros

---

## 📦 Componentes de Layout

### 1. PageContainer
Container principal para todas as páginas.

```jsx
import PageContainer from '../../components/layout/PageContainer'

<PageContainer className="max-w-7xl">
  {/* Conteúdo da página */}
</PageContainer>
```

**Props:**
- `children` - Conteúdo da página
- `className` - Classes adicionais (opcional)

### 2. PageHeader
Cabeçalho padrão com título, descrição e ações.

```jsx
import PageHeader from '../../components/layout/PageHeader'
import { Package } from 'lucide-react'

<PageHeader
  title="Inspeções"
  description="Gerencie todas as suas inspeções"
  icon={Package}
  showBackButton={true}
  backTo="/dashboard"
  actions={
    <Button icon={Plus}>Nova Inspeção</Button>
  }
/>
```

**Props:**
- `title` - Título da página (obrigatório)
- `description` - Descrição opcional
- `icon` - Ícone Lucide opcional
- `showBackButton` - Mostrar botão voltar (default: false)
- `backTo` - URL para voltar (opcional)
- `actions` - Botões de ação (opcional)

### 3. Card
Container de conteúdo com sombra e bordas arredondadas.

```jsx
import Card from '../../components/layout/Card'

<Card padding="default" hover={true}>
  {/* Conteúdo */}
</Card>
```

**Props:**
- `children` - Conteúdo do card
- `padding` - 'none' | 'sm' | 'default' | 'lg' (default: 'default')
- `hover` - Efeito hover (default: false)
- `className` - Classes adicionais

### 4. EmptyState
Estado vazio padrão para listas vazias.

```jsx
import EmptyState from '../../components/layout/EmptyState'
import { Package } from 'lucide-react'

<EmptyState
  icon={Package}
  title="Nenhuma inspeção encontrada"
  description="Comece criando sua primeira inspeção"
  action={
    <Button icon={Plus}>Nova Inspeção</Button>
  }
/>
```

**Props:**
- `icon` - Ícone Lucide
- `title` - Título do estado vazio
- `description` - Descrição opcional
- `action` - Botão de ação opcional

---

## 🔘 Componente Button

Botão padrão com variantes e estados.

```jsx
import Button from '../../components/ui/Button'
import { Plus } from 'lucide-react'

<Button 
  variant="primary"
  size="md"
  icon={Plus}
  iconPosition="left"
  loading={false}
  disabled={false}
  onClick={handleClick}
>
  Texto do Botão
</Button>
```

### Variantes:
- **primary** - Azul gradiente (ações principais)
- **secondary** - Branco com borda (ações secundárias)
- **danger** - Vermelho (exclusões, ações destrutivas)
- **success** - Verde (confirmações)
- **ghost** - Transparente (ações sutis)
- **link** - Estilo de link

### Tamanhos:
- **sm** - Pequeno (px-3 py-1.5)
- **md** - Médio (px-6 py-3) - padrão
- **lg** - Grande (px-8 py-4)

### Exemplos:

```jsx
{/* Botão primário com ícone */}
<Button icon={Plus}>Nova Inspeção</Button>

{/* Botão secundário */}
<Button variant="secondary">Cancelar</Button>

{/* Botão de perigo */}
<Button variant="danger" icon={Trash}>Excluir</Button>

{/* Botão com loading */}
<Button loading={isLoading}>Salvando...</Button>

{/* Botão desabilitado */}
<Button disabled>Não disponível</Button>
```

---

## 📝 Formulários

### Input Text Padrão
```jsx
<div>
  <label htmlFor="field" className="block text-sm font-medium text-gray-700">
    Label do Campo *
  </label>
  <input
    type="text"
    id="field"
    name="field"
    value={value}
    onChange={handleChange}
    placeholder="Ex: Texto exemplo"
    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
  />
</div>
```

### Select Padrão
```jsx
<div>
  <label htmlFor="select" className="block text-sm font-medium text-gray-700">
    Selecione uma opção *
  </label>
  <select
    id="select"
    name="select"
    value={value}
    onChange={handleChange}
    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
  >
    <option value="">Selecione...</option>
    <option value="1">Opção 1</option>
  </select>
</div>
```

### Textarea Padrão
```jsx
<div>
  <label htmlFor="textarea" className="block text-sm font-medium text-gray-700">
    Descrição
  </label>
  <textarea
    id="textarea"
    name="textarea"
    rows={3}
    value={value}
    onChange={handleChange}
    placeholder="Digite aqui..."
    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
  />
</div>
```

---

## 🎭 Ícones

Usamos **Lucide React** para ícones.

### Ícones Comuns:
```jsx
import {
  Package,      // Inspeções, containers
  Plus,         // Adicionar
  Search,       // Buscar
  Edit,         // Editar
  Trash,        // Excluir
  Eye,          // Visualizar
  Download,     // Download
  Upload,       // Upload
  Check,        // Sucesso
  X,            // Fechar, cancelar
  AlertTriangle,// Aviso
  Info,         // Informação
  ArrowLeft,    // Voltar
  ArrowRight,   // Próximo
  ChevronDown,  // Dropdown
  Filter,       // Filtrar
  Calendar,     // Data
  Clock,        // Tempo
  User,         // Usuário
  Settings,     // Configurações
} from 'lucide-react'
```

### Tamanhos Padrão:
- **h-4 w-4** - Pequeno (16px)
- **h-5 w-5** - Médio (20px) - padrão
- **h-6 w-6** - Grande (24px)
- **h-8 w-8** - Extra grande (32px)

---

## 📱 Responsividade

### Breakpoints Tailwind:
```
sm: 640px   - Tablet pequeno
md: 768px   - Tablet
lg: 1024px  - Desktop
xl: 1280px  - Desktop grande
2xl: 1536px - Desktop extra grande
```

### Exemplo de Grid Responsivo:
```jsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* Cards */}
</div>
```

---

## 🎬 Animações e Transições

### Transições Padrão:
```css
transition-all duration-200  /* Rápida */
transition-all duration-300  /* Média */
transition-all duration-500  /* Lenta */
```

### Efeitos Hover:
```jsx
{/* Escala */}
<div className="transform hover:scale-105 transition-transform">

{/* Sombra */}
<div className="shadow-md hover:shadow-xl transition-shadow">

{/* Cor */}
<div className="text-gray-600 hover:text-gray-900 transition-colors">
```

---

## 📋 Estrutura de Página Padrão

```jsx
import PageContainer from '../../components/layout/PageContainer'
import PageHeader from '../../components/layout/PageHeader'
import Card from '../../components/layout/Card'
import Button from '../../components/ui/Button'
import { IconName } from 'lucide-react'

export default function MyPage() {
  return (
    <PageContainer>
      {/* Header */}
      <PageHeader
        title="Título da Página"
        description="Descrição da página"
        icon={IconName}
        showBackButton={false}
        actions={
          <Button icon={Plus}>Ação Principal</Button>
        }
      />

      {/* Conteúdo */}
      <Card>
        {/* Seu conteúdo aqui */}
      </Card>
    </PageContainer>
  )
}
```

---

## ✅ Checklist de Consistência

Ao criar uma nova página, verifique:

- [ ] Usa `PageContainer` como wrapper principal
- [ ] Usa `PageHeader` para título e ações
- [ ] Usa `Card` para blocos de conteúdo
- [ ] Usa `Button` para todas as ações
- [ ] Usa `EmptyState` para listas vazias
- [ ] Ícones são do Lucide React
- [ ] Cores seguem a paleta definida
- [ ] Inputs seguem o padrão de formulário
- [ ] Espaçamentos consistentes (gap-4, gap-6, mb-6, etc.)
- [ ] Responsivo em todos os tamanhos de tela

---

## 🎯 Exemplos de Páginas

### Lista de Itens
```jsx
<PageContainer>
  <PageHeader
    title="Itens"
    description="Lista de todos os itens"
    icon={Package}
    actions={<Button icon={Plus}>Novo Item</Button>}
  />
  
  <Card padding="sm" className="mb-6">
    {/* Barra de busca */}
  </Card>
  
  <Card padding="none">
    {items.length === 0 ? (
      <EmptyState
        icon={Package}
        title="Nenhum item encontrado"
        description="Comece criando um novo item"
        action={<Button icon={Plus}>Novo Item</Button>}
      />
    ) : (
      <div className="divide-y divide-gray-200">
        {/* Lista de itens */}
      </div>
    )}
  </Card>
</PageContainer>
```

### Formulário
```jsx
<PageContainer className="max-w-4xl">
  <PageHeader
    title="Novo Item"
    description="Preencha as informações"
    icon={Package}
    showBackButton
  />
  
  <Card>
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Campos do formulário */}
      
      <div className="flex justify-end gap-3 mt-6">
        <Button variant="secondary" onClick={handleCancel}>
          Cancelar
        </Button>
        <Button type="submit" loading={loading}>
          Salvar
        </Button>
      </div>
    </form>
  </Card>
</PageContainer>
```

---

## 📚 Recursos

- **Tailwind CSS**: https://tailwindcss.com/docs
- **Lucide Icons**: https://lucide.dev/icons
- **React Router**: https://reactrouter.com

---

**Última atualização:** 25 de novembro de 2024
