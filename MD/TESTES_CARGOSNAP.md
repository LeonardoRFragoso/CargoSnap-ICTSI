# 🧪 Guia de Testes - Integração CargoSnap

Este documento descreve como testar a integração com a API do CargoSnap.

## 📝 Ordem dos Testes

Execute os testes na seguinte ordem:

### 1️⃣ Teste Simples da API (Sem Django)

Este teste verifica se a API do CargoSnap está respondendo corretamente, sem necessidade do Django rodando.

```bash
cd backend
python test_api_simple.py
```

**O que este teste verifica:**
- ✅ Conexão com a API do CargoSnap
- ✅ Primeira chamada (lista de arquivos)
- ✅ Segunda chamada (detalhes de um arquivo)
- ✅ Paginação funcionando
- ✅ Token válido

**Tempo estimado:** 10-30 segundos

**Resultado esperado:**
```
TESTE DA API CARGOSNAP
========================================
✓ API do CargoSnap está funcionando!
✓ Ambas as chamadas estão retornando dados
✓ Paginação está funcionando
```

---

### 2️⃣ Teste Completo com Django

Este teste verifica toda a integração: API, banco de dados, sincronização e download de imagens.

```bash
cd backend
python test_cargosnap_integration.py
```

**O que este teste verifica:**
- ✅ Conexão com API
- ✅ Modelos do banco de dados
- ✅ Sincronização de um arquivo
- ✅ Download de imagens
- ✅ Salvamento de dados completos

**Tempo estimado:** 1-3 minutos

**Resultado esperado:**
```
RESULTADO DOS TESTES
========================================
✓ PASSOU - Conexão API
✓ PASSOU - Modelos DB
✓ PASSOU - Sincronização
✓ PASSOU - Download Imagens

Total: 4/4 testes passaram

🎉 TODOS OS TESTES PASSARAM! Sistema funcionando corretamente.
```

---

### 3️⃣ Sincronização Completa

Após os testes passarem, execute a sincronização completa para baixar todos os dados.

```bash
cd backend
python manage.py sync_cargosnap
```

**Opções disponíveis:**

**Sincronização completa (com imagens):**
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

**Tempo estimado:** 
- Sem imagens: 2-5 minutos
- Com imagens: 10-30 minutos (dependendo da quantidade)

---

### 4️⃣ Testar no Frontend

1. **Inicie o backend:**
```bash
cd backend
python manage.py runserver
```

2. **Inicie o frontend (em outro terminal):**
```bash
cd frontend
npm run dev
```

3. **Acesse no navegador:**
```
http://localhost:5173/cargosnap
```

4. **Teste as funcionalidades:**
- ✅ Visualizar lista de containers
- ✅ Filtrar por código, status, avarias
- ✅ Ver detalhes de um container
- ✅ Visualizar galeria de fotos
- ✅ Clicar para ver imagem em tamanho completo
- ✅ Botão de sincronização
- ✅ Estatísticas no topo da página

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'requests'"

**Solução:**
```bash
pip install requests==2.31.0
```

### Erro: "Connection timeout" ou "Connection refused"

**Possíveis causas:**
1. Sem conexão com internet
2. API do CargoSnap fora do ar
3. Token inválido

**Verificação:**
```bash
# Teste manualmente
curl "https://api.cargosnap.com/api/v2/files?token=eW15Y1FGeXRqOEZRa3AxRlFRcXRMaGJyVmxMQjRVM3FfMTMwNQ==&limit=1"
```

### Erro: "TypeError: Cannot read properties of undefined"

**Já corrigido!** Este era o erro no frontend que foi resolvido.

### Erro: "No such table: cargosnap_files"

**Solução:**
```bash
cd backend
python manage.py makemigrations cargosnap_integration
python manage.py migrate
```

### Download de imagens muito lento

**É normal!** O download de imagens pode demorar dependendo de:
- Quantidade de imagens
- Tamanho das imagens
- Velocidade da internet

**Dica:** Use `--no-images` para sincronizar primeiro os dados, depois baixe as imagens:
```bash
python manage.py sync_cargosnap --no-images
# Depois, via interface, clique em "Baixar Imagens" em cada arquivo
```

---

## 📊 Verificando Resultados

### Via Admin Django

1. Acesse: `http://localhost:8000/admin/`
2. Login com superusuário
3. Navegue até "CargoSnap Integration"
4. Você verá:
   - Arquivos CargoSnap
   - Uploads (Imagens)
   - Workflows
   - Logs de Sincronização

### Via API

**Estatísticas:**
```bash
curl -X GET "http://localhost:8000/api/cargosnap/files/stats/" \
  -H "Authorization: Bearer {seu_token}"
```

**Lista de arquivos:**
```bash
curl -X GET "http://localhost:8000/api/cargosnap/files/" \
  -H "Authorization: Bearer {seu_token}"
```

### Via Banco de Dados

**SQLite:**
```bash
cd backend
sqlite3 db.sqlite3

# Consultas úteis:
SELECT COUNT(*) FROM cargosnap_files;
SELECT COUNT(*) FROM cargosnap_uploads;
SELECT COUNT(*) FROM cargosnap_uploads WHERE image_downloaded = 1;
```

---

## 📈 Métricas de Sucesso

Após executar todos os testes, você deve ter:

✅ **API**
- Conexão estabelecida
- Dados retornando corretamente

✅ **Banco de Dados**
- 37 arquivos (containers) salvos
- ~200-300 uploads (imagens) salvos
- Workflows salvos
- Logs de sincronização registrados

✅ **Imagens**
- Imagens salvas em `backend/media/cargosnap/images/`
- Thumbnails em `backend/media/cargosnap/thumbs/`

✅ **Frontend**
- Interface carregando
- Lista de containers visível
- Detalhes acessíveis
- Galeria funcionando

---

## 🎯 Checklist Final

Antes de considerar o sistema pronto:

- [ ] Teste simples da API passou
- [ ] Teste completo com Django passou
- [ ] Sincronização completa executada
- [ ] Pelo menos 10 imagens baixadas
- [ ] Frontend acessível e funcional
- [ ] Filtros funcionando
- [ ] Galeria de fotos funcionando
- [ ] Admin Django acessível
- [ ] Logs registrados

---

## 💡 Dicas

1. **Execute os testes nesta ordem** para identificar problemas rapidamente
2. **Guarde os logs** em caso de erro: `backend/logs/django.log`
3. **Teste primeiro com poucos dados** antes de sincronizar tudo
4. **Use `--page 1`** para testar sincronização de uma página primeiro
5. **Monitore o espaço em disco** ao baixar imagens

---

## 🆘 Suporte

Se algum teste falhar:

1. ✅ Verifique a mensagem de erro
2. ✅ Consulte a seção Troubleshooting acima
3. ✅ Verifique os logs: `backend/logs/django.log`
4. ✅ Execute os testes em modo debug
5. ✅ Verifique a documentação: `MD/CARGOSNAP_INTEGRATION.md`

---

**Última atualização:** 25/11/2024
