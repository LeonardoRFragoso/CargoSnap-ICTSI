# 📚 CargoSnap ICTSI - Guia Completo de APIs

## 🔗 Base URL
```
http://localhost:8000/api/
```

## 🔐 Autenticação

### Obter Token JWT
```http
POST /auth/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "senha123"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@ictsi.com",
    "full_name": "Admin User",
    "role": "ADMIN",
    "company": {
      "id": 1,
      "name": "ICTSI",
      "slug": "ictsi",
      "company_type": "ICTSI"
    }
  }
}
```

### Refresh Token
```http
POST /auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Usar Token nas Requisições
```http
GET /inspections/inspections/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## 📋 INSPECTIONS API

### Inspection Types
```http
GET    /inspections/types/                 # List all
POST   /inspections/types/                 # Create
GET    /inspections/types/{id}/            # Retrieve
PUT    /inspections/types/{id}/            # Update
DELETE /inspections/types/{id}/            # Delete
```

### Inspections
```http
GET    /inspections/inspections/           # List (com filtros)
POST   /inspections/inspections/           # Create
GET    /inspections/inspections/{id}/      # Detail
PUT    /inspections/inspections/{id}/      # Update
DELETE /inspections/inspections/{id}/      # Delete

# Actions
POST   /inspections/inspections/{id}/start/      # Start inspection
POST   /inspections/inspections/{id}/complete/   # Complete inspection
GET    /inspections/inspections/{id}/summary/    # Get summary
```

**Query Parameters:**
- `?status=COMPLETED` - Filter by status
- `?inspection_type=1` - Filter by type
- `?assigned_to=2` - Filter by assignee
- `?search=container` - Search in title, reference
- `?start_date=2024-01-01` - Filter by date
- `?ordering=-created_at` - Sort by field

### Photos
```http
GET    /inspections/photos/                # List
POST   /inspections/photos/                # Upload
GET    /inspections/photos/{id}/           # Retrieve
DELETE /inspections/photos/{id}/           # Delete
```

### Videos
```http
GET    /inspections/videos/                # List
POST   /inspections/videos/                # Upload
GET    /inspections/videos/{id}/           # Retrieve
DELETE /inspections/videos/{id}/           # Delete
```

### Documents
```http
GET    /inspections/documents/             # List
POST   /inspections/documents/             # Upload
GET    /inspections/documents/{id}/        # Retrieve
DELETE /inspections/documents/{id}/        # Delete
```

### Tags
```http
GET    /inspections/tags/                  # List
POST   /inspections/tags/                  # Create
GET    /inspections/tags/{id}/             # Retrieve
PUT    /inspections/tags/{id}/             # Update
DELETE /inspections/tags/{id}/             # Delete
```

### Signatures
```http
GET    /inspections/signatures/            # List
POST   /inspections/signatures/            # Create
GET    /inspections/signatures/{id}/       # Retrieve
DELETE /inspections/signatures/{id}/       # Delete
```

### Scanned References
```http
GET    /inspections/scanned-references/    # List
POST   /inspections/scanned-references/    # Create
GET    /inspections/scanned-references/{id}/ # Retrieve
```

### Container Structures (64 predefined)
```http
GET    /inspections/structures/            # List all 64
GET    /inspections/structures/{id}/       # Retrieve
```

**Query Parameters:**
- `?group=STRUCTURAL` - Filter by group
- `?is_critical=true` - Only critical parts
- `?search=porta` - Search by name

### Damage Types (46 predefined)
```http
GET    /inspections/damage-types/          # List all 46
GET    /inspections/damage-types/{id}/     # Retrieve
```

**Query Parameters:**
- `?default_severity=MAJOR` - Filter by severity
- `?affects_operation=true` - Only operational impacts

### Structure Inspection Items
```http
GET    /inspections/structure-items/       # List
POST   /inspections/structure-items/       # Create
GET    /inspections/structure-items/{id}/  # Retrieve
PUT    /inspections/structure-items/{id}/  # Update
```

### Checklists
```http
GET    /inspections/checklists/            # List
POST   /inspections/checklists/            # Create
GET    /inspections/checklists/{id}/       # Retrieve
PUT    /inspections/checklists/{id}/       # Update
```

---

## 🔄 WORKFLOWS API

### Workflows
```http
GET    /workflows/workflows/               # List
POST   /workflows/workflows/               # Create
GET    /workflows/workflows/{id}/          # Detail
PUT    /workflows/workflows/{id}/          # Update
DELETE /workflows/workflows/{id}/          # Delete

# Actions
POST   /workflows/workflows/{id}/duplicate/ # Duplicate workflow
```

### Workflow Steps
```http
GET    /workflows/steps/                   # List
POST   /workflows/steps/                   # Create
GET    /workflows/steps/{id}/              # Retrieve
PUT    /workflows/steps/{id}/              # Update
DELETE /workflows/steps/{id}/              # Delete
```

### Forms
```http
GET    /workflows/forms/                   # List
POST   /workflows/forms/                   # Create
GET    /workflows/forms/{id}/              # Retrieve
PUT    /workflows/forms/{id}/              # Update
```

### Form Fields
```http
GET    /workflows/form-fields/             # List
POST   /workflows/form-fields/             # Create
GET    /workflows/form-fields/{id}/        # Retrieve
PUT    /workflows/form-fields/{id}/        # Update
```

### Workflow Executions
```http
GET    /workflows/executions/              # List
POST   /workflows/executions/              # Create
GET    /workflows/executions/{id}/         # Retrieve

# Actions
POST   /workflows/executions/{id}/start/     # Start execution
POST   /workflows/executions/{id}/complete/  # Complete execution
```

---

## 📊 REPORTS API

### Report Templates
```http
GET    /reports/templates/                 # List
POST   /reports/templates/                 # Create
GET    /reports/templates/{id}/            # Detail
PUT    /reports/templates/{id}/            # Update
DELETE /reports/templates/{id}/            # Delete
```

### Reports
```http
GET    /reports/reports/                   # List
GET    /reports/reports/{id}/              # Detail
DELETE /reports/reports/{id}/              # Delete

# Actions
POST   /reports/reports/generate/          # Generate new report
POST   /reports/reports/{id}/share/        # Share report
```

**Generate Report Request:**
```json
{
  "inspection_id": 1,
  "template_id": 1
}
```

### Report Shares
```http
GET    /reports/shares/                    # List
POST   /reports/shares/                    # Create
GET    /reports/shares/{id}/               # Retrieve
```

### Report Annotations
```http
GET    /reports/annotations/               # List
POST   /reports/annotations/               # Create
GET    /reports/annotations/{id}/          # Retrieve

# Actions
POST   /reports/annotations/{id}/resolve/  # Resolve annotation
```

### Report Schedules
```http
GET    /reports/schedules/                 # List
POST   /reports/schedules/                 # Create
GET    /reports/schedules/{id}/            # Retrieve
PUT    /reports/schedules/{id}/            # Update

# Actions
POST   /reports/schedules/{id}/run_now/    # Execute immediately
```

---

## 🐛 ISSUES API

### Issue Categories
```http
GET    /issues/categories/                 # List
POST   /issues/categories/                 # Create
GET    /issues/categories/{id}/            # Retrieve
PUT    /issues/categories/{id}/            # Update
```

### Issues
```http
GET    /issues/issues/                     # List
POST   /issues/issues/                     # Create
GET    /issues/issues/{id}/                # Detail
PUT    /issues/issues/{id}/                # Update
DELETE /issues/issues/{id}/                # Delete

# Actions
POST   /issues/issues/{id}/resolve/        # Resolve issue
POST   /issues/issues/{id}/close/          # Close issue
```

**Query Parameters:**
- `?status=OPEN` - Filter by status
- `?priority=HIGH` - Filter by priority
- `?severity=CRITICAL` - Filter by severity
- `?assigned_to=2` - Filter by assignee

### Issue Photos
```http
GET    /issues/photos/                     # List
POST   /issues/photos/                     # Upload
GET    /issues/photos/{id}/                # Retrieve
```

### Issue Comments
```http
GET    /issues/comments/                   # List
POST   /issues/comments/                   # Create
GET    /issues/comments/{id}/              # Retrieve
```

### Issue Tasks
```http
GET    /issues/tasks/                      # List
POST   /issues/tasks/                      # Create
GET    /issues/tasks/{id}/                 # Retrieve
PUT    /issues/tasks/{id}/                 # Update
```

---

## 📈 ANALYTICS API

### Dashboard
```http
GET    /analytics/analytics/dashboard/            # Main dashboard stats
GET    /analytics/analytics/inspections_by_status/   # Grouped by status
GET    /analytics/analytics/issues_by_priority/      # Grouped by priority
GET    /analytics/analytics/inspections_timeline/    # Timeline chart
```

**Dashboard Response:**
```json
{
  "total_inspections": 150,
  "completed_inspections": 120,
  "pending_inspections": 30,
  "total_issues": 45,
  "open_issues": 12,
  "resolved_issues": 33,
  "total_reports": 100,
  "recent_inspections": [...]
}
```

---

## 🔔 CORE API

### Users
```http
GET    /auth/users/                        # List
POST   /auth/users/                        # Create
GET    /auth/users/{id}/                   # Retrieve
PUT    /auth/users/{id}/                   # Update

# Actions
GET    /auth/users/me/                     # Current user
PUT    /auth/users/update_profile/         # Update profile
POST   /auth/users/change_password/        # Change password
```

### Notifications
```http
GET    /auth/notifications/                # List my notifications
POST   /auth/notifications/{id}/mark_as_read/   # Mark as read
POST   /auth/notifications/mark_all_as_read/    # Mark all as read
GET    /auth/notifications/unread_count/        # Get unread count
```

### Webhooks
```http
GET    /auth/webhooks/                     # List
POST   /auth/webhooks/                     # Create
GET    /auth/webhooks/{id}/                # Retrieve
PUT    /auth/webhooks/{id}/                # Update
DELETE /auth/webhooks/{id}/                # Delete

# Actions
POST   /auth/webhooks/{id}/test/           # Test webhook
```

### API Keys
```http
GET    /auth/api-keys/                     # List
POST   /auth/api-keys/                     # Create
GET    /auth/api-keys/{id}/                # Retrieve
DELETE /auth/api-keys/{id}/                # Delete
```

---

## 🎯 Exemplos de Uso

### 1. Criar Inspeção Completa
```javascript
// 1. Create inspection
const inspectionRes = await fetch('/api/inspections/inspections/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    inspection_type: 1,
    title: "Inspeção Container ABCD1234",
    description: "Inspeção de recebimento",
    status: "DRAFT"
  })
});
const inspection = await inspectionRes.json();

// 2. Upload photo
const formData = new FormData();
formData.append('inspection', inspection.id);
formData.append('photo', photoFile);
formData.append('title', 'Foto frontal');

await fetch('/api/inspections/photos/', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` },
  body: formData
});

// 3. Start inspection
await fetch(`/api/inspections/inspections/${inspection.id}/start/`, {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` }
});

// 4. Complete inspection
await fetch(`/api/inspections/inspections/${inspection.id}/complete/`, {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` }
});
```

### 2. Filtrar e Buscar
```javascript
// Search and filter
const params = new URLSearchParams({
  status: 'COMPLETED',
  start_date: '2024-01-01',
  end_date: '2024-12-31',
  search: 'container',
  ordering: '-created_at'
});

const res = await fetch(`/api/inspections/inspections/?${params}`, {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

### 3. Upload Múltiplos Arquivos
```javascript
// Upload multiple photos
for (const photo of photos) {
  const formData = new FormData();
  formData.append('inspection', inspectionId);
  formData.append('photo', photo.file);
  formData.append('sequence_number', photo.sequence);
  
  await fetch('/api/inspections/photos/', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData
  });
}
```

---

## 📝 Status Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `204 No Content` - Success (no response body)
- `400 Bad Request` - Validation error
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - No permission
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## 🎓 Dicas

1. **Sempre use filtros** para reduzir o tamanho da resposta
2. **Paginação** automática em listas grandes
3. **Ordenação** com `?ordering=field` ou `-field` para desc
4. **Busca** com `?search=termo` em campos configurados
5. **Múltiplos filtros** podem ser combinados com `&`

---

## 📚 Recursos Adicionais

- Documentação interativa: http://localhost:8000/api/docs/
- Schema OpenAPI: http://localhost:8000/api/schema/
- Admin Django: http://localhost:8000/admin/
