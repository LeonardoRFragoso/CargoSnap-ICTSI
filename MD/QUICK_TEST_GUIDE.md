# 🧪 Guia Rápido de Teste - Sistema de Workflows

## ✅ Rota Atualizada!

A rota `/inspections/new` agora usa o novo componente `CreateInspectionWithWorkflow` com suporte completo a workflows e captura de fotos via câmera.

---

## 🚀 Como Testar

### 1. Iniciar o Frontend

```bash
cd frontend
npm run dev
```

Acesse: `http://localhost:5173`

### 2. Fazer Login

Use as credenciais configuradas no backend.

### 3. Criar Nova Inspeção

1. Clique em **"Inspeções"** no menu
2. Clique em **"Nova Inspeção"**
3. Você verá a nova interface:

```
┌─────────────────────────────────────┐
│ Nova Inspeção                       │
│ Preencha as informações básicas...  │
├─────────────────────────────────────┤
│ Tipo de Inspeção *                  │
│ [Inspeção de Carga ▼]              │
│                                     │
│ 📋 Workflow: Inspeção Padrão        │
│    4 passos a serem executados      │
│                                     │
│ Título *                            │
│ [Ex: Inspeção Container...]         │
│                                     │
│ Referência Externa                  │
│ [Ex: BL123456...]                   │
│                                     │
│ [Cancelar] [Criar e Iniciar →]     │
└─────────────────────────────────────┘
```

### 4. Executar Workflow

Após criar, você será levado para a execução do workflow:

```
┌─────────────────────────────────────┐
│ Workflow: Inspeção Container        │
│ Step 1 de 4                         │
│ ████████░░░░░░░░░░░░ 25%           │
├─────────────────────────────────────┤
│                                     │
│ [Formulário Dinâmico]               │
│                                     │
├─────────────────────────────────────┤
│ [← Anterior]    [Próximo →]        │
└─────────────────────────────────────┘
```

### 5. Testar Captura de Fotos

Quando chegar em um step de PHOTO:

1. Clique em **"Capturar Foto"**
2. Permita acesso à câmera quando solicitado
3. Tire a foto
4. Confirme ou refaça
5. Repita até atingir o mínimo necessário

---

## 🎯 O que Testar

### ✅ Funcionalidades Básicas

- [ ] Seleção de tipo de inspeção
- [ ] Visualização do workflow associado
- [ ] Criação da inspeção
- [ ] Navegação entre steps
- [ ] Barra de progresso

### ✅ Formulários Dinâmicos

- [ ] Campos de texto
- [ ] Campos numéricos
- [ ] Selects/Dropdowns
- [ ] Checkboxes
- [ ] Validação de campos obrigatórios
- [ ] Mensagens de erro

### ✅ Captura de Fotos

- [ ] Abrir câmera
- [ ] Capturar foto
- [ ] Preview da foto
- [ ] Refazer foto
- [ ] Confirmar foto
- [ ] Trocar câmera (frontal/traseira)
- [ ] Upload da galeria
- [ ] Validação de mínimo/máximo
- [ ] Contador de fotos

### ✅ Navegação

- [ ] Botão "Anterior"
- [ ] Botão "Próximo"
- [ ] Botão "Pular" (se permitido)
- [ ] Botão "Concluir" no último step
- [ ] Validação antes de avançar

### ✅ Conclusão

- [ ] Upload de fotos
- [ ] Salvamento de dados
- [ ] Notificação de sucesso
- [ ] Redirecionamento

---

## 🐛 Troubleshooting

### Problema: Câmera não abre

**Solução:**
- Verifique se o navegador tem permissão para acessar a câmera
- Use HTTPS (em produção)
- Teste em navegador diferente (Chrome recomendado)

### Problema: Workflow não carrega

**Solução:**
1. Verifique se o backend está rodando
2. Abra o console (F12) e veja os logs
3. Verifique se existem workflows cadastrados no banco

```bash
# No backend
python manage.py shell

from apps.workflows.models import Workflow
print(Workflow.objects.all())
```

### Problema: Tipos de inspeção vazios

**Solução:**
1. Verifique se existem tipos cadastrados
2. O sistema usa fallback automático se não houver tipos

```bash
# No backend
python manage.py shell

from apps.inspections.models import InspectionType
print(InspectionType.objects.all())
```

---

## 📝 Criar Workflow de Teste

Se não houver workflows cadastrados, crie um de teste:

```python
# No Django shell
from apps.core.models import Company
from apps.inspections.models import InspectionType
from apps.workflows.models import Workflow, WorkflowStep, WorkflowForm, WorkflowFormField

# Pegar empresa e tipo
company = Company.objects.first()
inspection_type = InspectionType.objects.first()

# Criar workflow
workflow = Workflow.objects.create(
    company=company,
    name="Inspeção de Teste",
    code="TEST_INSPECTION",
    inspection_type=inspection_type,
    is_default=True,
    is_active=True
)

# Step 1: Formulário
step1 = WorkflowStep.objects.create(
    workflow=workflow,
    name="Dados Básicos",
    step_type="FORM",
    sequence=1,
    is_required=True
)

form1 = WorkflowForm.objects.create(
    company=company,
    name="Informações Gerais",
    code="GENERAL_INFO"
)

WorkflowFormField.objects.create(
    form=form1,
    label="Número de Referência",
    field_type="TEXT",
    is_required=True,
    sequence=1
)

WorkflowFormField.objects.create(
    form=form1,
    label="Quantidade",
    field_type="NUMBER",
    is_required=True,
    sequence=2
)

step1.form_links.create(form=form1)

# Step 2: Fotos
step2 = WorkflowStep.objects.create(
    workflow=workflow,
    name="Fotos Gerais",
    step_type="PHOTO",
    sequence=2,
    is_required=True,
    min_photos=2,
    max_photos=5
)

print("Workflow criado com sucesso!")
print(f"ID: {workflow.id}")
print(f"Steps: {workflow.steps.count()}")
```

---

## 📱 Teste em Dispositivo Móvel

### Opção 1: Usando IP Local

1. Encontre seu IP local:
   ```bash
   # Windows
   ipconfig
   
   # Mac/Linux
   ifconfig
   ```

2. Inicie o frontend com host 0.0.0.0:
   ```bash
   npm run dev -- --host
   ```

3. Acesse do celular:
   ```
   http://SEU_IP:5173
   ```

### Opção 2: Usando ngrok

```bash
# Instalar ngrok
npm install -g ngrok

# Expor porta
ngrok http 5173
```

---

## ✅ Checklist de Teste Completo

### Desktop
- [ ] Chrome
- [ ] Firefox
- [ ] Edge
- [ ] Safari (Mac)

### Mobile
- [ ] Chrome Android
- [ ] Safari iOS
- [ ] Samsung Internet

### Funcionalidades
- [ ] Criar inspeção sem workflow
- [ ] Criar inspeção com workflow
- [ ] Executar todos os steps
- [ ] Capturar fotos via câmera
- [ ] Upload fotos da galeria
- [ ] Validações de formulário
- [ ] Navegação entre steps
- [ ] Conclusão do workflow
- [ ] Upload de fotos
- [ ] Redirecionamento

---

## 📊 Logs Úteis

Abra o Console (F12) e procure por:

```
Fetching inspection types...
Inspection types received: [...]
Loading workflow for type: X
Workflows received: [...]
Selected workflow: {...}
```

Se houver erros, eles aparecerão em vermelho no console.

---

## 🎉 Sucesso!

Se tudo funcionar:
- ✅ Formulário carrega
- ✅ Workflow é exibido
- ✅ Steps são executados
- ✅ Câmera funciona
- ✅ Fotos são capturadas
- ✅ Inspeção é concluída

**Parabéns! O sistema está funcionando perfeitamente! 🚀**

---

**Última atualização:** 25/11/2024
**Versão:** 2.0.0
