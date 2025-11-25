# 🔄 Como Configurar os Workflows Padrão

## ❓ Por que a mensagem "Nenhum workflow configurado" aparece?

A mensagem aparece porque os workflows padrão ainda não foram criados no banco de dados. O sistema está funcionando corretamente, mas precisa que você execute um comando para popular os workflows.

---

## ✅ Solução Rápida

### Opção 1: Executar o Comando Django (Recomendado)

**1. Abra o terminal no diretório do backend:**
```bash
cd backend
```

**2. Ative o ambiente virtual:**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**3. Execute o comando para criar workflows:**
```bash
python manage.py create_default_workflows
```

**4. Reinicie o servidor se estiver rodando**

---

### Opção 2: Criar Workflows Manualmente pelo Admin

**1. Acesse o Django Admin:**
```
http://localhost:8000/admin/
```

**2. Faça login com suas credenciais de admin**

**3. Vá em "Workflows" → "Workflows"**

**4. Clique em "Adicionar Workflow"**

**5. Preencha:**
- **Nome**: Inspeção Padrão de Container
- **Tipo de Inspeção**: Inspeção de Container
- **Descrição**: Workflow completo para inspeção de containers
- **Ativo**: ✓
- **Padrão**: ✓

**6. Salve e adicione passos (WorkflowSteps)**

---

### Opção 3: Criar via API (Para Desenvolvedores)

```javascript
// 1. Criar Workflow
const workflow = await fetch('http://localhost:8000/api/workflows/workflows/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Inspeção Padrão de Container',
    inspection_type: 1, // ID do tipo de inspeção
    description: 'Workflow completo para inspeção de containers',
    is_active: true,
    is_default: true
  })
})

// 2. Criar Steps do Workflow
const step1 = await fetch('http://localhost:8000/api/workflows/steps/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    workflow: workflow.id,
    name: 'Identificação do Container',
    description: 'Registre os dados do container',
    step_type: 'FORM',
    sequence_order: 1,
    is_required: true
  })
})
```

---

## 📋 Workflows que Serão Criados

### 1. Workflow de Inspeção de Container
**5 Passos:**
1. ✅ Identificação do Container (Formulário)
2. 📸 Fotos Externas (4-20 fotos)
3. ✅ Inspeção Estrutural (Checklist)
4. 📸 Fotos Internas (3-15 fotos)
5. ⚠️ Registro de Danos (Opcional)

### 2. Workflow de Inspeção de Carga
**3 Passos:**
1. ✅ Identificação da Carga (Formulário)
2. 📸 Fotos Gerais (3-20 fotos)
3. ✅ Verificação de Condições (Checklist)

### 3. Workflow de Inspeção de Veículo
**3 Passos:**
1. ✅ Identificação do Veículo (Formulário)
2. 📸 Fotos Externas (6-20 fotos)
3. ✅ Inspeção Visual (Checklist)

---

## 🔍 Como Verificar se os Workflows Foram Criados

### Via Django Admin:
1. Acesse: `http://localhost:8000/admin/workflows/workflow/`
2. Você deve ver 3 workflows listados

### Via API:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/workflows/workflows/
```

### Via Frontend:
1. Acesse: `http://localhost:5173/inspections/new`
2. Selecione um tipo de inspeção
3. Você deve ver uma caixa azul com "Workflow: [Nome]" e número de passos

---

## 🐛 Troubleshooting

### Erro: "No module named 'django'"
**Solução:** Ative o ambiente virtual primeiro
```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### Erro: "Company matching query does not exist"
**Solução:** Crie uma empresa primeiro via Django Admin ou execute:
```bash
python manage.py createsuperuser
# Depois faça login no admin e crie uma empresa
```

### Erro: "InspectionType matching query does not exist"
**Solução:** O comando cria os tipos automaticamente. Se persistir:
```bash
python manage.py shell
>>> from apps.core.models import Company
>>> from apps.inspections.models import InspectionType
>>> company = Company.objects.first()
>>> InspectionType.objects.create(
...     company=company,
...     code='CONTAINER',
...     name='Inspeção de Container',
...     description='Inspeção de containers marítimos'
... )
```

### Workflows não aparecem no frontend
**Possíveis causas:**
1. ✅ Verifique se o backend está rodando
2. ✅ Verifique se você está autenticado
3. ✅ Verifique o console do navegador para erros de API
4. ✅ Verifique se os workflows estão marcados como `is_active=True`

---

## 📝 Comandos Úteis

```bash
# Ver todos os workflows
python manage.py shell
>>> from apps.workflows.models import Workflow
>>> Workflow.objects.all()

# Ver workflows por tipo de inspeção
>>> Workflow.objects.filter(inspection_type__code='CONTAINER')

# Deletar todos os workflows (cuidado!)
>>> Workflow.objects.all().delete()

# Recriar workflows
>>> exit()
python manage.py create_default_workflows
```

---

## 🚀 Próximos Passos Após Criar Workflows

1. ✅ Teste criar uma nova inspeção
2. ✅ Verifique se o workflow aparece
3. ✅ Execute o workflow completo
4. ✅ Verifique se as fotos são salvas
5. ✅ Verifique se a inspeção é concluída

---

## 💡 Dica Pro

Para desenvolvimento, você pode adicionar este comando ao seu script de setup:

**setup.ps1 (Windows):**
```powershell
# Adicione após as migrações
Write-Host "Criando workflows padrão..." -ForegroundColor Cyan
python manage.py create_default_workflows
```

**setup.sh (Linux/Mac):**
```bash
# Adicione após as migrações
echo "Criando workflows padrão..."
python manage.py create_default_workflows
```

---

**Última atualização:** 25 de novembro de 2024
