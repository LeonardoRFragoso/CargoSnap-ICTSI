# 🔄 Implementação de Workflows por Tipo de Inspeção

## Conceito

No CargoSnap original, cada **Tipo de Inspeção** pode ter um **Workflow específico** com formulários dinâmicos customizados.

## Estrutura Atual do Projeto

### ✅ Já Implementado no Backend

```
Workflow
├── inspection_type (FK) ← Associa workflow a tipo de inspeção
├── is_default (bool) ← Workflow padrão para o tipo
├── WorkflowStep[] ← Passos do workflow
│   ├── step_type (FORM, PHOTO, VIDEO, SCAN, SIGNATURE)
│   ├── WorkflowForm ← Formulário customizado
│   │   └── WorkflowFormField[] ← Campos do formulário
│   │       ├── field_type (TEXT, NUMBER, SELECT, etc.)
│   │       ├── is_required
│   │       ├── validation rules
│   │       └── conditional logic
│   └── sequence (ordem)
└── WorkflowExecution ← Execução do workflow na inspeção
```

## 🎯 Implementação Sugerida no Frontend

### Fase 1: Carregar Workflow ao Selecionar Tipo

```javascript
// CreateInspection.jsx

const [selectedWorkflow, setSelectedWorkflow] = useState(null)
const [workflowSteps, setWorkflowSteps] = useState([])

// Quando tipo de inspeção mudar
useEffect(() => {
  if (formData.inspection_type) {
    loadWorkflowForType(formData.inspection_type)
  }
}, [formData.inspection_type])

const loadWorkflowForType = async (typeId) => {
  try {
    // Buscar workflow padrão para o tipo
    const workflows = await workflowService.getByInspectionType(typeId)
    const defaultWorkflow = workflows.find(w => w.is_default) || workflows[0]
    
    if (defaultWorkflow) {
      setSelectedWorkflow(defaultWorkflow)
      setWorkflowSteps(defaultWorkflow.steps)
    }
  } catch (err) {
    console.error('Error loading workflow:', err)
  }
}
```

### Fase 2: Renderizar Formulários Dinâmicos

```javascript
// DynamicForm.jsx

export default function DynamicForm({ workflow, onComplete }) {
  const [currentStep, setCurrentStep] = useState(0)
  const [formData, setFormData] = useState({})
  
  const renderField = (field) => {
    switch (field.field_type) {
      case 'TEXT':
        return <input type="text" {...field} />
      case 'NUMBER':
        return <input type="number" {...field} />
      case 'SELECT':
        return (
          <select>
            {field.options.map(opt => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        )
      case 'CHECKBOX':
        return <input type="checkbox" {...field} />
      // ... outros tipos
    }
  }
  
  return (
    <div>
      <h3>Step {currentStep + 1}: {workflowSteps[currentStep].name}</h3>
      
      {workflowSteps[currentStep].forms.map(form => (
        <div key={form.id}>
          {form.fields.map(field => (
            <div key={field.id}>
              <label>{field.label}</label>
              {renderField(field)}
            </div>
          ))}
        </div>
      ))}
      
      <button onClick={nextStep}>Próximo</button>
    </div>
  )
}
```

### Fase 3: Exemplos de Workflows por Tipo

#### Workflow: Inspeção de Container
```json
{
  "name": "Inspeção de Container Padrão",
  "inspection_type": 2,
  "is_default": true,
  "steps": [
    {
      "sequence": 1,
      "name": "Dados do Container",
      "step_type": "FORM",
      "form": {
        "fields": [
          { "label": "Número do Container", "field_type": "TEXT", "is_required": true },
          { "label": "Tipo", "field_type": "SELECT", "options": ["20ft", "40ft", "40ft HC"] },
          { "label": "Condição", "field_type": "SELECT", "options": ["Vazio", "Cheio"] }
        ]
      }
    },
    {
      "sequence": 2,
      "name": "Fotos das 6 Faces",
      "step_type": "PHOTO",
      "min_photos": 6,
      "max_photos": 6
    },
    {
      "sequence": 3,
      "name": "Checklist de Estruturas",
      "step_type": "FORM",
      "form": {
        "fields": [
          { "label": "Porta Direita", "field_type": "SELECT", "options": ["OK", "Danificado"] },
          { "label": "Porta Esquerda", "field_type": "SELECT", "options": ["OK", "Danificado"] },
          { "label": "Teto", "field_type": "SELECT", "options": ["OK", "Danificado"] }
        ]
      }
    },
    {
      "sequence": 4,
      "name": "Assinatura",
      "step_type": "SIGNATURE"
    }
  ]
}
```

#### Workflow: Inspeção de Carga
```json
{
  "name": "Inspeção de Carga Padrão",
  "inspection_type": 1,
  "is_default": true,
  "steps": [
    {
      "sequence": 1,
      "name": "Dados da Carga",
      "step_type": "FORM",
      "form": {
        "fields": [
          { "label": "Tipo de Carga", "field_type": "TEXT", "is_required": true },
          { "label": "Peso (kg)", "field_type": "NUMBER", "is_required": true },
          { "label": "Volume (m³)", "field_type": "NUMBER" },
          { "label": "Embalagem", "field_type": "SELECT", "options": ["Palete", "Caixa", "Granel"] }
        ]
      }
    },
    {
      "sequence": 2,
      "name": "Fotos Gerais",
      "step_type": "PHOTO",
      "min_photos": 3
    },
    {
      "sequence": 3,
      "name": "Contagem",
      "step_type": "FORM",
      "form": {
        "fields": [
          { "label": "Quantidade de Volumes", "field_type": "NUMBER", "is_required": true },
          { "label": "Observações", "field_type": "TEXTAREA" }
        ]
      }
    }
  ]
}
```

## 📊 Endpoints Necessários

### Backend (já implementado)
```python
# apps/workflows/views.py

GET  /api/workflows/workflows/                    # Listar todos
GET  /api/workflows/workflows/?inspection_type=2  # Filtrar por tipo
GET  /api/workflows/workflows/{id}/               # Detalhes
POST /api/workflows/executions/                   # Iniciar execução
POST /api/workflows/executions/{id}/complete/     # Completar
```

### Frontend (a implementar)
```javascript
// services/workflowService.js

export const workflowService = {
  getAll: async () => { ... },
  getByInspectionType: async (typeId) => {
    const response = await api.get('/workflows/workflows/', {
      params: { inspection_type: typeId }
    })
    return response.data
  },
  getById: async (id) => { ... },
  startExecution: async (workflowId, inspectionId) => { ... },
  completeStep: async (executionId, stepId, data) => { ... }
}
```

## 🎯 Roadmap de Implementação

### Fase 1: Básico (1-2 dias)
- [ ] Criar serviço de workflows no frontend
- [ ] Carregar workflow ao selecionar tipo de inspeção
- [ ] Mostrar nome e descrição do workflow selecionado

### Fase 2: Formulários Dinâmicos (3-5 dias)
- [ ] Componente DynamicForm
- [ ] Renderização de 14 tipos de campos
- [ ] Validações customizadas
- [ ] Navegação entre steps

### Fase 3: Execução (2-3 dias)
- [ ] Salvar respostas dos formulários
- [ ] Tracking de progresso
- [ ] Upload de fotos por step
- [ ] Assinaturas digitais

### Fase 4: Avançado (5-7 dias)
- [ ] Lógica condicional (campos que aparecem baseado em respostas)
- [ ] Workflows com aprovação
- [ ] Relatórios baseados em workflow
- [ ] Editor visual de workflows (admin)

## 🎨 UI/UX Sugerida

### Seletor de Tipo com Preview do Workflow
```
┌─────────────────────────────────────┐
│ Tipo de Inspeção *                  │
│ ┌─────────────────────────────────┐ │
│ │ Inspeção de Container          ▼│ │
│ └─────────────────────────────────┘ │
│                                     │
│ 📋 Workflow: Inspeção Container     │
│    Padrão (4 passos)                │
│                                     │
│ Steps:                              │
│ 1. ✏️  Dados do Container           │
│ 2. 📷 Fotos das 6 Faces             │
│ 3. ✅ Checklist de Estruturas       │
│ 4. ✍️  Assinatura                   │
└─────────────────────────────────────┘
```

### Execução do Workflow
```
┌─────────────────────────────────────┐
│ Inspeção Container ABCD1234         │
│                                     │
│ Progresso: ████████░░░░ 2/4 (50%)  │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Step 2: Fotos das 6 Faces       │ │
│ │                                 │ │
│ │ Tire fotos de todas as faces:   │ │
│ │                                 │ │
│ │ [📷] [📷] [📷] [📷] [📷] [📷]   │ │
│ │  ✓    ✓    ✓    ✓    -    -    │ │
│ │                                 │ │
│ │ 4/6 fotos capturadas            │ │
│ └─────────────────────────────────┘ │
│                                     │
│ [← Voltar]  [Pular]  [Próximo →]   │
└─────────────────────────────────────┘
```

## 📝 Benefícios

✅ **Flexibilidade**: Cada tipo de inspeção tem seu próprio fluxo
✅ **Consistência**: Todos seguem o mesmo processo
✅ **Rastreabilidade**: Histórico completo de cada step
✅ **Validação**: Garante que todos os dados necessários foram coletados
✅ **Escalabilidade**: Fácil adicionar novos tipos e workflows

## 🚀 Próximo Passo Imediato

**Sugestão:** Implementar a Fase 1 primeiro - mostrar o workflow associado ao tipo de inspeção selecionado, sem ainda executá-lo. Isso dará uma prévia ao usuário do que será necessário coletar.

---

**Documentação criada em:** 25/11/2024
**Versão:** 1.0
