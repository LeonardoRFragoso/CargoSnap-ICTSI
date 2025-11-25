# Funcionalidades Implementadas - CargoSnap ICTSI

Este documento detalha todas as funcionalidades implementadas no sistema CargoSnap ICTSI, baseadas na análise do CargoSnap original.

## 📋 Índice

1. [Inspeções (Inspections)](#1-inspeções-inspections)
2. [Fluxos de Trabalho (Workflows)](#2-fluxos-de-trabalho-workflows)
3. [Relatórios (Reports)](#3-relatórios-reports)
4. [Gestão de Ocorrências (Issues)](#4-gestão-de-ocorrências-issues)
5. [Notificações e Webhooks](#5-notificações-e-webhooks)
6. [Sistema Multi-Tenant](#6-sistema-multi-tenant)

---

## 1. Inspeções (Inspections)

### Modelos Implementados

#### `InspectionType`
- **Propósito**: Tipos de inspeções configuráveis por empresa
- **Recursos**:
  - Nome, código e descrição
  - Ícone e cor personalizáveis
  - Ativo/inativo por empresa

#### `Inspection`
- **Propósito**: Registro principal de inspeção
- **Recursos**:
  - **Referências**: Número de referência único, referência externa
  - **Status**: Rascunho, Em Andamento, Concluída, Aprovada, Rejeitada, Cancelada
  - **Atribuição**: Atribuído a, Inspetor
  - **Localização**: GPS (latitude/longitude), endereço
  - **Dados Ambientais**: Clima, temperatura
  - **Datas**: Agendada, Iniciada, Concluída
  - **Cliente**: Nome, email, telefone
  - **Campos Customizados**: JSON para flexibilidade

#### `InspectionPhoto`
- **Propósito**: Fotos capturadas durante inspeção
- **Recursos**:
  - Upload de fotos com thumbnails
  - Metadados: título, descrição, legenda
  - GPS e informações do dispositivo
  - Sequenciamento e foto de capa
  - Organizadas por data

#### `InspectionVideo`
- **Propósito**: Vídeos da inspeção
- **Recursos**:
  - Suporta: mp4, mov, avi, mkv
  - Thumbnail automático
  - Duração e tamanho do arquivo
  - Metadados completos

#### `InspectionDocument`
- **Propósito**: Documentos anexos
- **Recursos**:
  - Tipos: PDF, Excel, Word, Imagem, Outros
  - Controle de tamanho
  - Rastreamento de upload (usuário)

#### `InspectionTag`
- **Propósito**: Tags/Etiquetas para organização
- **Recursos**:
  - Nome e cor personalizáveis
  - Por empresa
  - Many-to-many com inspeções

#### `InspectionSignature`
- **Propósito**: Assinaturas digitais
- **Recursos**:
  - Tipos: Inspetor, Supervisor, Cliente, Testemunha
  - Imagem da assinatura
  - Dados do signatário (nome, email, função)
  - IP e user agent para auditoria

#### `InspectionComment`
- **Propósito**: Comentários e notas
- **Recursos**:
  - Internos vs visíveis ao cliente
  - Comentários em thread (respostas)
  - Rastreamento por usuário

#### `ScannedReference`
- **Propósito**: Scanner de códigos
- **Recursos**:
  - Tipos: Barcode, QR Code, Placa, Número de Container, Número de Selo
  - Validação de dados
  - Rastreamento de quem escaneou

---

## 2. Fluxos de Trabalho (Workflows)

### Modelos Implementados

#### `Workflow`
- **Propósito**: Template de fluxo de trabalho
- **Recursos**:
  - Nome, código e versão
  - Associado a tipo de inspeção
  - Configurações: Requer aprovação, Permite pular steps, Gera relatório automaticamente
  - Workflow padrão por tipo

#### `WorkflowStep`
- **Propósito**: Passos individuais do workflow
- **Recursos**:
  - **Tipos de Step**: 
    - Preencher Formulário
    - Tirar Foto
    - Gravar Vídeo
    - Escanear Referência
    - Coletar Assinatura
    - Aprovação Necessária
    - Enviar Notificação
    - Ação Customizada
  - **Lógica Condicional**: Campo, operador, valor para mostrar/ocultar
  - Sequenciamento
  - Obrigatório/pulável
  - Limites de fotos (min/max)

#### `WorkflowForm`
- **Propósito**: Formulários customizáveis
- **Recursos**:
  - Nome, código e descrição
  - Campos dinâmicos
  - Reutilizável entre workflows

#### `WorkflowFormField`
- **Propósito**: Campos do formulário
- **Recursos**:
  - **Tipos**: Text, Number, Date, Time, DateTime, TextArea, Select, MultiSelect, Checkbox, Radio, Email, Phone, URL, File
  - **Validação**: Obrigatório, min/max value, min/max length, pattern regex
  - **Opções**: Para selects e radios
  - **Display Condicional**: Mostrar se outro campo = valor
  - Largura customizável (full, half, third, quarter)
  - Valor padrão

#### `WorkflowExecution`
- **Propósito**: Rastreamento de execução
- **Recursos**:
  - Status: Não Iniciado, Em Progresso, Concluído, Falhou, Cancelado
  - Progresso (step atual / total)
  - Datas de início e conclusão
  - Dados coletados (JSON)

#### `WorkflowStepExecution`
- **Propósito**: Execução de steps individuais
- **Recursos**:
  - Status por step
  - Tempo de execução
  - Dados coletados
  - Notas

#### `WorkflowFormResponse`
- **Propósito**: Respostas aos formulários
- **Recursos**:
  - Valor e URL de arquivo
  - Rastreamento de quem respondeu
  - Timestamp

---

## 3. Relatórios (Reports)

### Modelos Implementados

#### `ReportTemplate`
- **Propósito**: Templates de relatório
- **Recursos**:
  - **Formatos**: PDF, Excel, Word, HTML, JSON
  - **Template**: Arquivo ou HTML
  - **Seções Incluídas**: 
    - Capa
    - Resumo
    - Fotos
    - Assinaturas
    - Comentários
    - Metadados
  - **Customização**:
    - Logo
    - Cabeçalho/rodapé
    - Marca d'água
    - Estilos (JSON)
  - Template padrão por tipo de inspeção
  - Versionamento

#### `Report`
- **Propósito**: Relatórios gerados
- **Recursos**:
  - Status: Gerando, Concluído, Falhou, Arquivado
  - Arquivo e tamanho
  - Tempo de geração
  - **Compartilhamento**:
    - Público/privado
    - URL pública
    - Código de acesso
  - Versionamento (parent_report)
  - Mensagem de erro se falhou

#### `ReportSection`
- **Propósito**: Seções customizadas
- **Recursos**:
  - Título e descrição
  - Tipo de conteúdo (fotos, tabela, texto, gráfico)
  - Configuração (JSON)
  - Quebras de página
  - Habilitado/desabilitado

#### `ReportShare`
- **Propósito**: Compartilhamento de relatórios
- **Recursos**:
  - Email e nome do destinatário
  - Permissões (download, impressão)
  - Data de expiração
  - Rastreamento de acesso
  - Mensagem personalizada

#### `ReportAnnotation`
- **Propósito**: Anotações em relatórios
- **Recursos**:
  - Texto e posição (x, y)
  - Número de página e seção
  - Status: Resolvido/não resolvido
  - Quem resolveu e quando

#### `ReportSchedule`
- **Propósito**: Agendamento automático
- **Recursos**:
  - **Frequências**: Diária, Semanal, Mensal, Trimestral, Ao Completar, Ao Aprovar
  - Filtros (tipo, status, range de datas)
  - Lista de destinatários
  - Próxima execução
  - Estatísticas de execução

---

## 4. Gestão de Ocorrências (Issues)

### Modelos Implementados

#### `IssueCategory`
- **Propósito**: Categorias de problemas
- **Recursos**:
  - Nome, descrição, cor, ícone
  - Prioridade padrão
  - SLA padrão (horas)
  - Por empresa

#### `Issue`
- **Propósito**: Registro de problemas
- **Recursos**:
  - **Classificação**:
    - Prioridade: Baixa, Média, Alta, Crítica
    - Severidade: Menor, Moderada, Maior, Crítica
    - Status: Aberto, Em Progresso, Resolvido, Fechado, Reaberto
  - **Atribuição**:
    - Reportado por
    - Atribuído a (usuário)
    - Time atribuído
  - **Localização**: GPS e endereço
  - **Datas**: Detectado, Vencimento, Resolvido, Fechado
  - **Resolução**:
    - Notas de resolução
    - Causa raiz
    - Ação preventiva
  - **Impacto Financeiro**: Custo estimado e real
  - Número de referência único
  - Campos customizados (JSON)

#### `IssuePhoto`
- **Propósito**: Documentação fotográfica
- **Recursos**:
  - Tipos: Antes, Depois, Evidência, Outro
  - Legenda
  - Sequenciamento
  - Thumbnail

#### `IssueComment`
- **Propósito**: Comentários e atualizações
- **Recursos**:
  - Interno vs visível ao cliente
  - Anexos
  - Rastreamento por usuário

#### `IssueAttachment`
- **Propósito**: Arquivos anexos
- **Recursos**:
  - Nome, tamanho, tipo
  - Upload organizado por data

#### `IssueTask`
- **Propósito**: Tarefas de resolução
- **Recursos**:
  - Status: A Fazer, Em Progresso, Concluída, Cancelada
  - Atribuição
  - Data de vencimento
  - Sequenciamento

#### `IssueHistory`
- **Propósito**: Auditoria de mudanças
- **Recursos**:
  - Ação, campo alterado
  - Valor antigo e novo
  - IP e timestamp
  - Rastreamento completo

#### `IssueTemplate`
- **Propósito**: Templates de problemas comuns
- **Recursos**:
  - Descrição template
  - Valores padrão
  - Checklist items
  - Contador de uso

---

## 5. Notificações e Webhooks

### Modelos Implementados

#### `Notification`
- **Propósito**: Notificações do sistema
- **Recursos**:
  - **Tipos**: Info, Sucesso, Aviso, Erro, Tarefa, Menção, Lembrete
  - **Canais**: In-App, Email, SMS, Push
  - Título e mensagem
  - Link de ação
  - Status lido/não lido
  - Relação com objeto (model + id)
  - Metadados (JSON)

#### `Webhook`
- **Propósito**: Integrações externas
- **Recursos**:
  - **Eventos**:
    - inspection.created, updated, completed, approved
    - issue.created, resolved
    - report.generated
    - workflow.completed
  - URL e secret key
  - Headers customizados
  - Retry automático (configurável)
  - **Estatísticas**:
    - Total de chamadas
    - Sucesso/falha
    - Último status
  - Ativo/inativo

#### `WebhookLog`
- **Propósito**: Log de chamadas
- **Recursos**:
  - Payload e headers
  - Status code e resposta
  - Tempo de resposta (ms)
  - Sucesso/erro
  - Número de tentativa
  - Timestamp completo

#### `ApiKey`
- **Propósito**: API Keys para integração
- **Recursos**:
  - Nome e descrição
  - Key gerada automaticamente
  - Lista de permissões (JSON)
  - Rate limiting (por hora)
  - Data de expiração
  - **Estatísticas**:
    - Último uso
    - Total de requisições
  - Ativo/inativo

---

## 6. Sistema Multi-Tenant

### Modelos Core

#### `Company`
- **Propósito**: Empresas do grupo
- **Recursos**:
  - Tipos: ICTSI, iTracker, CLIA
  - Informações de contato completas
  - Endereço completo
  - Logo e cores personalizadas
  - Slug único
  - Ativo/inativo

#### `User` (Custom)
- **Propósito**: Usuários do sistema
- **Recursos**:
  - Extends AbstractUser
  - Associado a company (multi-tenant)
  - **Roles**: Admin, Manager, Inspector, Viewer, Client
  - Avatar, telefone
  - Idioma e timezone
  - Propriedades auxiliares (full_name, can_create_inspections)

#### `AuditLog`
- **Propósito**: Log de auditoria
- **Recursos**:
  - Tipos de ação: Create, Update, Delete, View, Export
  - Modelo e ID do objeto
  - Descrição
  - IP e User Agent
  - Por usuário e empresa

#### `BaseModel`
- **Propósito**: Modelo abstrato
- **Recursos**:
  - created_at
  - updated_at
  - Usado por todos os modelos principais

---

## 📊 Resumo Estatístico

### Total de Modelos Implementados: **47 modelos**

| App | Modelos | Descrição |
|-----|---------|-----------|
| **Core** | 7 | Company, User, AuditLog, BaseModel, Notification, Webhook, WebhookLog, ApiKey |
| **Inspections** | 10 | InspectionType, Inspection, Photo, Video, Document, Tag, TagRelation, Signature, Comment, ScannedReference |
| **Workflows** | 9 | Workflow, WorkflowStep, Form, FormField, StepForm, Execution, StepExecution, FormResponse |
| **Reports** | 6 | Template, Report, Section, Share, Annotation, Schedule |
| **Issues** | 8 | Category, Issue, Photo, Comment, Attachment, Task, History, Template |
| **Analytics** | Placeholder | A implementar |

---

## 🔄 Funcionalidades Transversais

### 1. Scanner
- Barcodes
- QR Codes
- Placas de veículos
- Números de container
- Números de selo
- Validação automática

### 2. Tags & Labels
- Organização de inspeções
- Cores customizáveis
- Filtros e busca

### 3. Assinaturas Digitais
- Múltiplos signatários
- Tipos configuráveis
- Rastreamento completo

### 4. Compartilhamento
- Relatórios públicos/privados
- Código de acesso
- Permissões granulares
- Expiração automática

### 5. Lógica Condicional
- Workflows dinâmicos
- Formulários adaptativos
- Steps condicionais

### 6. Automação
- Relatórios agendados
- Webhooks por eventos
- Notificações automáticas
- Retry inteligente

---

## 🎯 Próximos Passos

1. **Serializers**: Criar serializers para todos os modelos
2. **Views**: Implementar ViewSets e views customizadas
3. **Permissions**: Sistema de permissões granular
4. **Testes**: Testes unitários e de integração
5. **Analytics**: Implementar dashboards e métricas
6. **Mobile**: Otimizações específicas para mobile
7. **PWA**: Suporte offline e instalação
8. **Performance**: Cache, índices, otimizações

---

## 📝 Notas Técnicas

### Campos JSON Utilizados
- `custom_fields`: Campos customizáveis
- `metadata`: Metadados adicionais
- `config`: Configurações específicas
- `options`: Opções de select/radio
- `styling`: Estilos de template
- `permissions`: Lista de permissões
- `data`: Dados genéricos

### Validações
- FileExtensionValidator para uploads
- Unique constraints para códigos e referências
- Índices para queries performáticas
- Choices para campos com valores limitados

### Segurança
- Multi-tenancy via middleware
- API Keys com rate limiting
- Webhook secret keys
- Audit logs completos
- IP tracking

