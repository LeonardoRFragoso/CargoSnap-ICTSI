# 📋 Campos Adicionados ao Sistema de Inspeção

## ✅ Resumo das Alterações

Foram adicionados campos específicos para cada tipo de inspeção, alinhados com os padrões da API oficial do CargoSnap.

---

## 🚢 Campos para Inspeção de Container/Carga

### Novos Campos no Modelo `Inspection`:

1. **container_number** - Número do container (ex: ABCD1234567)
2. **seal_number** - Número do lacre/selo
3. **booking_number** - Número de booking ou BL (Bill of Lading)
4. **vessel_name** - Nome do navio
5. **voyage_number** - Número da viagem
6. **container_type** - Tipo de container (20ft, 40ft, etc.)
7. **container_size** - Tamanho do container
8. **cargo_description** - Descrição detalhada da carga
9. **cargo_weight** - Peso da carga em kg

### Tipos de Container Disponíveis:
- 20ft Standard
- 40ft Standard
- 40ft High Cube
- 20ft Refrigerated
- 40ft Refrigerated
- 20ft Open Top
- 40ft Open Top
- 20ft Flat Rack
- 40ft Flat Rack

---

## 🚗 Campos para Inspeção de Veículo

### Novos Campos no Modelo `Inspection`:

1. **vehicle_plate** - Placa do veículo
2. **vehicle_model** - Modelo do veículo
3. **vehicle_year** - Ano do veículo
4. **vehicle_vin** - Número do chassi (VIN)

---

## 🔄 Workflows Padrão Criados

### 1. Workflow de Inspeção de Container

**Passos:**
1. **Identificação do Container**
   - Número do container
   - Número do lacre
   - Tipo de container

2. **Fotos Externas**
   - Mínimo: 4 fotos
   - Máximo: 20 fotos

3. **Inspeção Estrutural**
   - Condição das paredes
   - Condição do piso
   - Condição do teto
   - Portas funcionando
   - Vazamentos detectados
   - Observações

4. **Fotos Internas**
   - Mínimo: 3 fotos
   - Máximo: 15 fotos

5. **Registro de Danos** (opcional)
   - Tipo de dano
   - Localização
   - Severidade
   - Descrição detalhada

### 2. Workflow de Inspeção de Carga

**Passos:**
1. **Identificação da Carga**
   - Descrição da carga
   - Quantidade de volumes
   - Peso total
   - Tipo de embalagem

2. **Fotos Gerais da Carga**
   - Mínimo: 3 fotos
   - Máximo: 20 fotos

3. **Verificação de Condições**
   - Embalagem intacta
   - Sinais de umidade
   - Produtos danificados
   - Etiquetas legíveis
   - Observações

### 3. Workflow de Inspeção de Veículo

**Passos:**
1. **Identificação do Veículo**
   - Placa
   - Modelo
   - Ano
   - Cor
   - Chassi (VIN)

2. **Fotos Externas**
   - Mínimo: 6 fotos
   - Máximo: 20 fotos

3. **Inspeção Visual**
   - Condição da pintura
   - Pneus em bom estado
   - Vidros intactos
   - Faróis funcionando
   - Amassados ou arranhões
   - Observações

---

## 📝 Formulário Dinâmico

O formulário de criação de inspeção agora exibe campos específicos baseados no tipo de inspeção selecionado:

- **Inspeção de Container/Carga**: Exibe campos de container e carga
- **Inspeção de Veículo**: Exibe campos de veículo
- **Outros tipos**: Exibe apenas campos básicos

---

## 🗄️ Migração do Banco de Dados

Arquivo criado: `backend/apps/inspections/migrations/0002_add_container_vehicle_fields.py`

**Para aplicar a migração:**
```bash
cd backend
python manage.py migrate inspections
```

---

## 🎯 Comando para Criar Workflows Padrão

**Para popular os workflows padrão no banco:**
```bash
cd backend
python manage.py create_default_workflows
```

Este comando irá:
- Criar tipos de inspeção padrão (se não existirem)
- Criar workflows completos para cada tipo
- Criar formulários e campos associados
- Configurar passos de fotos e verificações

---

## 🔧 Arquivos Modificados

### Backend:
1. `backend/apps/inspections/models.py` - Adicionados novos campos
2. `backend/apps/inspections/serializers.py` - Atualizados serializers
3. `backend/apps/inspections/migrations/0002_add_container_vehicle_fields.py` - Nova migration
4. `backend/apps/workflows/management/commands/create_default_workflows.py` - Comando para workflows

### Frontend:
1. `frontend/src/pages/inspections/CreateInspectionWithWorkflow.jsx` - Formulário expandido com campos dinâmicos

---

## ✨ Melhorias Implementadas

1. ✅ Campos específicos por tipo de inspeção
2. ✅ Formulário dinâmico que adapta campos ao tipo selecionado
3. ✅ Workflows completos e prontos para uso
4. ✅ Validações apropriadas para cada campo
5. ✅ Interface organizada com seções separadas
6. ✅ Compatibilidade com padrões CargoSnap
7. ✅ Suporte para múltiplos tipos de container
8. ✅ Campos de rastreamento (booking, vessel, voyage)

---

## 🚀 Próximos Passos

Para começar a usar:

1. **Aplicar a migração do banco de dados:**
   ```bash
   cd backend
   python manage.py migrate inspections
   ```

2. **Criar workflows padrão:**
   ```bash
   python manage.py create_default_workflows
   ```

3. **Reiniciar o backend** (se estiver rodando)

4. **Testar no frontend:**
   - Acesse `/inspections/new`
   - Selecione um tipo de inspeção
   - Verifique os campos específicos aparecerem
   - Preencha e crie uma inspeção

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique se as migrações foram aplicadas
2. Confirme que os workflows foram criados
3. Verifique os logs do backend para erros
4. Teste com diferentes tipos de inspeção

---

**Última atualização:** 25 de novembro de 2024
