# 🔧 Troubleshooting - CargoSnap ICTSI

## Problema: Dropdown "Tipo de Inspeção" Vazio

### Sintoma
O select de "Tipo de Inspeção" aparece vazio na página de Nova Inspeção.

### Causa Raiz
1. **API não está respondendo** - Backend pode não estar rodando
2. **Formato de resposta inesperado** - API pode retornar dados em formato diferente
3. **Erro de autenticação** - Token JWT pode estar inválido
4. **CORS** - Problemas de Cross-Origin Resource Sharing

### Solução Implementada

#### 1. Melhor Tratamento de Resposta da API
```javascript
// Agora suporta múltiplos formatos de resposta:
- Array direto: [{ id: 1, name: '...' }]
- Com results: { results: [{ id: 1, name: '...' }] }
- Com data: { data: [{ id: 1, name: '...' }] }
```

#### 2. Fallback para Dados Mock
Se a API falhar, o sistema automaticamente usa dados padrão:
- Inspeção de Carga
- Inspeção de Container
- Inspeção de Veículo
- Inspeção de Recebimento
- Inspeção de Expedição

#### 3. Estados de Loading
- Mostra "Carregando tipos..." enquanto busca da API
- Desabilita o select durante carregamento
- Mostra mensagem de erro se nenhum tipo for encontrado

#### 4. Logs de Debug
Console logs adicionados para facilitar diagnóstico:
```javascript
console.log('Fetching inspection types...')
console.log('Inspection types received:', data)
console.log('Processed types:', types)
```

### Como Verificar

#### 1. Abra o Console do Navegador (F12)
Procure por mensagens:
- ✅ "Fetching inspection types..." - Iniciou busca
- ✅ "Inspection types received: ..." - Recebeu resposta
- ✅ "Processed types: ..." - Processou dados
- ⚠️ "No inspection types found..." - Nenhum tipo encontrado
- ❌ "Error loading inspection types..." - Erro na API

#### 2. Verifique se o Backend Está Rodando
```bash
# Deve responder com status 200
curl http://localhost:8000/api/inspections/types/
```

#### 3. Verifique Autenticação
- Faça login novamente se necessário
- Token JWT pode ter expirado

### Endpoints Relacionados

```
GET /api/inspections/types/
Authorization: Bearer {token}

Response esperado:
{
  "results": [
    {
      "id": 1,
      "name": "Inspeção de Carga",
      "code": "CARGO",
      "company": 1,
      "is_active": true
    }
  ]
}
```

### Próximos Passos

Se o problema persistir:

1. **Verificar Backend**
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Criar Tipos de Inspeção**
   ```bash
   python manage.py shell
   >>> from apps.inspections.models import InspectionType
   >>> from apps.core.models import Company
   >>> company = Company.objects.first()
   >>> InspectionType.objects.create(
   ...     company=company,
   ...     name='Inspeção de Carga',
   ...     code='CARGO'
   ... )
   ```

3. **Verificar Permissões**
   - Usuário deve ter permissão para listar tipos
   - Verificar role do usuário (ADMIN, MANAGER, etc.)

4. **Verificar CORS**
   - Backend deve permitir requisições do frontend
   - Verificar `CORS_ALLOWED_ORIGINS` em `settings.py`

### Arquivos Modificados

- `frontend/src/pages/inspections/CreateInspection.jsx`
  - Melhor tratamento de resposta da API
  - Fallback para dados mock
  - Estados de loading
  - Logs de debug

### Comportamento Atual

✅ **Com API funcionando**: Carrega tipos reais do backend
✅ **Sem API**: Usa dados padrão (5 tipos mock)
✅ **Durante carregamento**: Mostra "Carregando tipos..."
✅ **Erro**: Mostra notificação toast e usa fallback

---

**Data:** 25/11/2024
**Versão:** 1.0.1
**Status:** ✅ Resolvido
