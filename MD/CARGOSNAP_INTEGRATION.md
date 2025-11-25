# Integração CargoSnap - Documentação Completa

## 📋 Visão Geral

Esta documentação descreve a integração completa com a API do CargoSnap, implementada conforme solicitado. O sistema permite:

1. ✅ Buscar todos os dados da API do CargoSnap
2. ✅ Armazenar informações completas em tabelas estruturadas
3. ✅ Capturar todas as páginas da API (com paginação automática)
4. ✅ Gravar todos os dados da segunda chamada (detalhes completos)
5. ✅ Fazer download de todas as imagens automaticamente

## 🔧 Estrutura Técnica

### Backend (Django)

#### Modelos Criados

O sistema cria as seguintes tabelas no banco de dados:

1. **CargoSnapFile** - Arquivos principais (containers)
   - Informações básicas do container
   - Estatísticas de fotos e avarias
   - Status de sincronização

2. **CargoSnapUpload** - Fotos/Imagens
   - Metadados das fotos
   - URLs das imagens (original e thumbnail)
   - Caminhos dos arquivos baixados localmente
   - Informações de geolocalização
   - Dados de avarias

3. **CargoSnapWorkflow** - Workflows do sistema
   - Definições de workflows
   - Etapas do workflow

4. **CargoSnapWorkflowRun** - Execuções de workflows
   - Histórico de execuções
   - Status de conclusão

5. **CargoSnapLocation** - Localizações dos containers

6. **CargoSnapSyncLog** - Logs de sincronização
   - Histórico completo de sincronizações
   - Estatísticas de sucesso/erro

### APIs Disponíveis

Base URL: `http://localhost:8000/api/cargosnap/`

#### 1. Listar Arquivos
```
GET /api/cargosnap/files/
```

Parâmetros de filtro:
- `search`: Buscar por código do container
- `has_damage`: true/false - Filtrar por avarias
- `sync_status`: pending/syncing/completed/error
- `date_from`: Data inicial (YYYY-MM-DD)
- `date_to`: Data final (YYYY-MM-DD)

#### 2. Detalhes do Arquivo
```
GET /api/cargosnap/files/{id}/
```

Retorna:
- Dados completos do arquivo
- Todas as imagens (uploads)
- Workflows executados
- Localizações
- Estatísticas

#### 3. Sincronizar Arquivo Específico
```
POST /api/cargosnap/files/{id}/sync/
Body: { "download_images": true }
```

#### 4. Baixar Imagens de um Arquivo
```
POST /api/cargosnap/files/{id}/download_images/
```

#### 5. Estatísticas Gerais
```
GET /api/cargosnap/files/stats/
```

Retorna:
- Total de arquivos
- Total de imagens
- Imagens baixadas
- Arquivos com avarias
- Última sincronização

#### 6. Listar Uploads (Imagens)
```
GET /api/cargosnap/uploads/
```

Filtros:
- `file_id`: ID do arquivo
- `has_damage`: true/false
- `workflow_id`: ID do workflow
- `date_from` / `date_to`

#### 7. Listar Workflows
```
GET /api/cargosnap/workflows/
```

#### 8. Logs de Sincronização
```
GET /api/cargosnap/sync-logs/
```

#### 9. Iniciar Sincronização Completa
```
POST /api/cargosnap/sync-logs/trigger_sync/
Body: { "download_images": true }
```

## 🚀 Como Usar

### 1. Configuração Inicial

#### Backend
```bash
cd backend

# Instalar dependências
pip install -r requirements.txt

# Executar migrações
python manage.py makemigrations
python manage.py migrate

# Criar superusuário (se necessário)
python manage.py createsuperuser
```

#### Frontend
```bash
cd frontend

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev
```

### 2. Sincronização de Dados

#### Via Linha de Comando

**Sincronização completa (recomendado para primeira execução):**
```bash
python manage.py sync_cargosnap
```

**Sincronização sem baixar imagens:**
```bash
python manage.py sync_cargosnap --no-images
```

**Sincronizar arquivo específico:**
```bash
python manage.py sync_cargosnap --file-id 3524074
```

**Sincronizar página específica:**
```bash
python manage.py sync_cargosnap --page 1
```

#### Via Interface Web

1. Acesse o sistema: `http://localhost:5173`
2. Faça login
3. Navegue até "CargoSnap" no menu
4. Clique no botão "Sincronizar Dados"
5. Aguarde a conclusão (pode demorar alguns minutos)

#### Via API

```bash
curl -X POST http://localhost:8000/api/cargosnap/sync-logs/trigger_sync/ \
  -H "Authorization: Bearer {seu_token}" \
  -H "Content-Type: application/json" \
  -d '{"download_images": true}'
```

### 3. Acessando os Dados

#### Via Interface Web

**Lista de Containers:**
- Acesse: `http://localhost:5173/cargosnap`
- Filtros disponíveis:
  - Busca por código do container
  - Status de sincronização
  - Filtro de avarias
  - Intervalo de datas

**Detalhes do Container:**
- Clique em "Ver Detalhes" em qualquer container
- Visualize:
  - Todas as fotos em galeria
  - Workflows executados
  - Informações de localização
  - Estatísticas
- Funções:
  - Visualizar imagens em tamanho completo
  - Baixar imagens
  - Resincronizar dados

#### Via Admin Django

1. Acesse: `http://localhost:8000/admin/`
2. Navegue até "CargoSnap Integration"
3. Gerenciamento completo de:
   - Arquivos
   - Uploads (Imagens)
   - Workflows
   - Logs de sincronização

### 4. Localização das Imagens Baixadas

As imagens são salvas em:
```
backend/media/cargosnap/
  ├── images/      # Imagens completas
  └── thumbs/      # Thumbnails
```

Padrão de nomenclatura:
```
{scan_code}_{upload_id}_{timestamp}.jpg
```

Exemplo:
```
TCLU8075642_26382422_20220519_170611.jpg
```

## 📊 Estrutura de Dados

### Dados da Primeira Chamada (Lista)
```json
{
  "id": 3524074,
  "scan_code": "TCLU8075642",
  "scan_code_format": "NONE",
  "closed": 0,
  "created_at": "2022-05-19T17:06:17.540000Z",
  "updated_at": "2022-05-19T17:51:31.187000Z",
  "recent_snap_id": 26384952,
  "snap_count": 9,
  "snap_count_with_damage": 0
}
```

### Dados da Segunda Chamada (Detalhes)

Inclui tudo da primeira chamada, mais:

- **uploads[]**: Array com todas as fotos
  - Metadados completos
  - URLs das imagens
  - Geolocalização
  - Informações de workflow
  - Dados de avarias

- **workflow_runs[]**: Execuções de workflows
  - Workflow completo com steps
  - Status de execução
  - Timestamps

- **locations[]**: Localizações do container

- **form_submits[]**: Formulários submetidos

- **fields[]**: Campos customizados

## 🔍 Monitoramento

### Logs de Sincronização

Cada sincronização cria um registro de log com:
- Data/hora de início e fim
- Quantidade de arquivos processados
- Arquivos criados/atualizados
- Imagens baixadas
- Erros (se houver)

Acesse via:
- Admin Django: `/admin/cargosnap_integration/cargosnapsynclog/`
- API: `/api/cargosnap/sync-logs/`

### Status de Sincronização

Cada arquivo tem um status:
- **pending**: Aguardando sincronização
- **syncing**: Sendo sincronizado
- **completed**: Sincronizado com sucesso
- **error**: Erro na sincronização

## 🎯 Funcionalidades Implementadas

### ✅ Requisito 1: Criar Tabelas
- 10 tabelas criadas
- Relacionamentos definidos
- Índices otimizados
- Campos JSON para dados complexos

### ✅ Requisito 2: Capturar Todas as Páginas
- Detecção automática do total de páginas
- Processamento sequencial
- Controle de paginação
- Logs detalhados

### ✅ Requisito 3: Gravar Todos os Dados
- Sincronização completa de:
  - Dados básicos dos arquivos
  - Uploads (fotos)
  - Workflows e execuções
  - Localizações
  - Formulários
  - Campos customizados

### ✅ Requisito 4: Download de Imagens
- Download automático de imagens completas
- Download de thumbnails
- Organização em diretórios
- Nomenclatura padronizada
- Controle de status de download

## 🔐 Segurança

- Token de API armazenado no código do serviço
- Autenticação JWT para APIs
- Permissões por usuário
- CORS configurado

## 📈 Performance

- Paginação implementada (25 itens por página)
- Filtros otimizados com índices
- Caching de thumbnails
- Lazy loading de imagens no frontend

## 🐛 Troubleshooting

### Erro: "No module named 'requests'"
```bash
pip install requests==2.31.0
```

### Erro: Timeout na API
- Verifique conexão com internet
- Confirme que o token está correto
- Tente novamente após alguns minutos

### Imagens não aparecem
- Verifique se o download foi concluído
- Confirme permissões da pasta media/
- Verifique logs de erro

### Sincronização travada
- Verifique logs: `backend/logs/django.log`
- Reinicie o processo
- Use `--page` para sincronizar páginas específicas

## 📝 Próximos Passos (Opcional)

1. **Agendamento Automático**
   - Configurar Celery para sincronizações periódicas
   - Exemplo: Sincronizar a cada 1 hora

2. **Notificações**
   - Alertas quando novos containers com avarias forem detectados
   - Email quando sincronização falhar

3. **Exportação**
   - Exportar dados para Excel/PDF
   - Relatórios customizados

4. **Integração com Inspeções**
   - Vincular dados do CargoSnap com inspeções do sistema
   - Importar fotos automaticamente

## 💡 Dicas

- Execute a primeira sincronização em horário de baixo uso
- O download de imagens pode levar tempo dependendo da quantidade
- Use filtros para encontrar containers específicos rapidamente
- Monitore os logs para identificar problemas

## 🆘 Suporte

Em caso de dúvidas ou problemas:
1. Consulte esta documentação
2. Verifique os logs em `backend/logs/django.log`
3. Acesse o admin Django para dados detalhados
4. Use o endpoint `/api/cargosnap/files/stats/` para diagnóstico

---

**Implementado em:** 25 de Novembro de 2024
**Versão:** 1.0.0
**Status:** ✅ Produção
