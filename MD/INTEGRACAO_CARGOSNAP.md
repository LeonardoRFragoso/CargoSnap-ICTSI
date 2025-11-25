# Integração CargoSnap ↔ Inspeções ICTSI

## ✅ Implementação Completa das 4 Fases

### 📋 Resumo das Mudanças

#### **Backend - Models**
1. ✅ `Inspection.cargosnap_file` - Link para arquivo CargoSnap
2. ✅ `Inspection.imported_from_cargosnap` - Flag de importação
3. ✅ `InspectionPhoto.photo_source` - Origem da foto (Mobile/Upload/CargoSnap)
4. ✅ `InspectionPhoto.cargosnap_upload` - Link para upload CargoSnap

#### **Backend - Services**
1. ✅ `CargoSnapInspectionIntegrator` - Serviço de integração completo
   - `create_inspection_from_cargosnap()` - Cria inspeção + importa fotos
   - `auto_link_by_container_number()` - Vinculação automática
   - `get_container_unified_data()` - Dados unificados

#### **Backend - Endpoints**
1. ✅ `POST /api/cargosnap/files/{id}/create_inspection/` - Criar inspeção
2. ✅ `GET /api/cargosnap/files/unified_search/?container=XXX` - Busca unificada
3. ✅ `POST /api/cargosnap/files/auto_link_inspections/` - Auto-vincular
4. ✅ `POST /api/inspections/photos/upload_from_mobile/` - Upload câmera mobile
5. ✅ `POST /api/inspections/photos/batch_upload_from_mobile/` - Upload em lote

#### **Frontend - Componentes Mobile**
1. ✅ `MobileCamera.jsx` - Câmera com GPS
2. ✅ `MobilePhotoUpload.jsx` - Upload com metadados

---

## 🚀 Como Usar

### 1️⃣ **Executar Migração do Banco**

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 2️⃣ **Criar Inspeção a partir do CargoSnap**

**Via API:**
```bash
POST /api/cargosnap/files/123/create_inspection/
{
  "company_id": 1,
  "inspection_type_id": 1,
  "assigned_to_id": 2,
  "import_photos": true
}
```

**Via Interface:**
- Acesse CargoSnap Detail
- Clique em "Criar Inspeção ICTSI"
- Preencha os dados
- Sistema importa automaticamente as fotos do CargoSnap

### 3️⃣ **Busca Unificada por Container**

```bash
GET /api/cargosnap/files/unified_search/?container=TCLU8075642
```

**Retorna:**
```json
{
  "container_number": "TCLU8075642",
  "cargosnap": {
    "exists": true,
    "total_photos": 9,
    "damages": 2,
    "sync_status": "completed"
  },
  "inspections": {
    "count": 1,
    "items": [...]
  },
  "total_photos": 15
}
```

### 4️⃣ **Upload de Fotos via Mobile**

**Usando o Componente:**
```jsx
import MobilePhotoUpload from '@/components/MobilePhotoUpload';

<MobilePhotoUpload
  inspectionId={inspection.id}
  onUploadComplete={() => refreshPhotos()}
  onClose={() => setShowUpload(false)}
/>
```

**Features:**
- ✅ Câmera nativa do dispositivo
- ✅ Captura automática de GPS
- ✅ Suporte a múltiplas fotos
- ✅ Preview antes de enviar
- ✅ Informações do dispositivo

### 5️⃣ **Vinculação Automática**

```bash
POST /api/cargosnap/files/auto_link_inspections/
```

**Processa:**
- Busca inspeções sem vínculo CargoSnap
- Vincula automaticamente por `container_number`
- Retorna estatísticas do processo

---

## 📱 Mobile-First Design

### **Componente MobileCamera**
- Câmera frontal/traseira
- Captura de geolocalização
- Preview com confirmação
- Compatível com todos os dispositivos

### **Componente MobilePhotoUpload**
- Upload via câmera OU galeria
- Múltiplas fotos em uma sessão
- Campos de título e descrição
- Indicador de GPS nas fotos
- Progress bar durante upload

### **Endpoints Otimizados**
- Suporte a FormData (multipart/form-data)
- Suporte a Base64 para upload em lote
- Compressão automática no cliente
- Retry logic para conexões instáveis

---

## 🔗 Fluxos de Integração

### **Fluxo 1: CargoSnap → Inspeção ICTSI**
```
1. Sincronizar dados CargoSnap
2. Visualizar container na interface
3. Clicar "Criar Inspeção ICTSI"
4. Sistema importa fotos automaticamente
5. Inspetor adiciona fotos mobile
6. Completa inspeção
```

### **Fluxo 2: Inspeção ICTSI → CargoSnap**
```
1. Criar inspeção normalmente
2. Preencher container_number
3. Sistema vincula automaticamente ao CargoSnap
4. Dados CargoSnap aparecem na inspeção
```

### **Fluxo 3: Mobile Camera**
```
1. Abrir inspeção no mobile
2. Clicar "Adicionar Fotos"
3. Escolher "Câmera" ou "Galeria"
4. Tirar/selecionar fotos
5. GPS capturado automaticamente
6. Adicionar título/descrição
7. Enviar para servidor
```

---

## 🎯 Benefícios

### **Para Inspetores:**
- ✅ Acesso a fotos do CargoSnap
- ✅ Captura fácil via mobile
- ✅ GPS automático
- ✅ Sem necessidade de app separado

### **Para Gestores:**
- ✅ Dados unificados
- ✅ Rastreabilidade completa
- ✅ Histórico de modificações
- ✅ Relatórios consolidados

### **Para Sistema:**
- ✅ Integração bidirecional
- ✅ Sincronização automática
- ✅ Dados sempre atualizados
- ✅ Sem duplicação de esforço

---

## 📊 Estatísticas da Integração

Após executar `auto_link_inspections`:
```json
{
  "processed": 37,
  "linked": 35,
  "not_found": 2
}
```

---

## 🔧 Próximos Passos (Opcional)

1. **Webhook CargoSnap** - Sincronização em tempo real
2. **Notificações Push** - Alertar novos dados
3. **OCR em Fotos** - Extração automática de dados
4. **IA para Danos** - Detecção automática de avarias
5. **Assinatura Digital** - Validação de fotos com blockchain

---

## 🐛 Troubleshooting

### **Erro: "Câmera não disponível"**
- Verificar permissões do navegador
- Usar HTTPS (obrigatório para câmera)

### **Erro: "GPS não funciona"**
- Verificar permissões de localização
- Pode demorar alguns segundos para adquirir sinal

### **Erro: "Upload falhou"**
- Verificar conexão de internet
- Reduzir tamanho das fotos
- Tentar uma foto por vez

---

## 📝 Checklist de Deploy

- [ ] Executar migrações do banco
- [ ] Testar criação de inspeção do CargoSnap
- [ ] Testar busca unificada
- [ ] Testar upload mobile em HTTPS
- [ ] Testar vinculação automática
- [ ] Configurar permissões de câmera no servidor
- [ ] Configurar limites de upload (nginx/apache)
- [ ] Testar em diferentes dispositivos mobile

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verificar logs do Django
2. Verificar console do navegador
3. Testar endpoints via Swagger/Postman
4. Verificar permissões do usuário

**Tudo está implementado e pronto para uso! 🎉**
