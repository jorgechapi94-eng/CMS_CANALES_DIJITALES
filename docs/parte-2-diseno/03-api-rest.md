# 2.3 Diseño de API REST — Portal CMS UPEC

**Especificación OpenAPI 3.0.3:** [`openapi.yaml`](./openapi.yaml)  
**Runtime:** Flask 3.1 / Python 3.12 · cliente: Vue 3 (Node.js) vía Axios  
**Base URL local:** `http://localhost:5000`

La práctica pide **al menos 5 endpoints**. El contrato cubre los módulos Auth, News, Programs, Newspapers, YouTube y Radio (más de 5), alineado con los blueprints reales de `backend/app/api/`.

---

## Prompt usado con la IA

```
Genera OpenAPI 3.0 para el CMS UPEC (SPA + Flask).
Mínimo 5 endpoints. Incluye:
- POST /api/auth/login (JWT, solo @upec.edu.ec)
- CRUD noticias y programas
- multipart para PDF del periódico
- GET público de YouTube y radio status
Verifica verbos HTTP, códigos 200/201/400/401/403/404/500,
payloads JSON y errores { "error": "..." }.
No expongas la API Key de YouTube. No uses GET para login.
```

---

## Endpoints principales (contrato)

| Método | Ruta | Auth / rol | Éxito | Errores |
|---|---|---|---|---|
| `POST` | `/api/auth/login` | Público | **200** `{access_token, refresh_token, user}` | 400 sin campos, **401** credenciales, **403** dominio o inactivo |
| `GET` | `/api/news` | Público (solo `published`) | **200** página `{items,total,pages,current_page}` | — |
| `GET` | `/api/news/{slug}` | Público | **200** noticia + `content_html` | **404** |
| `POST` | `/api/news` | JWT `editor` \| `superadmin` | **201** | 400, 401, 403 |
| `PUT` | `/api/news/{id}` | JWT `editor` \| `superadmin` | **200** | 401, 403, 404 |
| `DELETE` | `/api/news/{id}` | JWT `editor` \| `superadmin` | **200** `{message}` | 401, 403, 404 |
| `GET` | `/api/programs/{id}` | Público | **200** ficha con docentes/estudiantes/proyectos | **404** |
| `POST` | `/api/programs` | JWT `gestor_programas` \| `superadmin` | **201** | 400, 401, 403 |
| `POST` | `/api/newspapers` | JWT `editor` \| `superadmin` | **201** `multipart/form-data` | 400 archivo/fecha, 401, 403 |
| `GET` | `/api/youtube/latest` | Público | **200** array de videos | **500** si no hay key/playlist y no hay caché |
| `GET` | `/api/radio/status` | Público | **200** metadatos o fallback | no 502: degradación suave |

Convenciones:

- JSON UTF-8; fechas ISO-8601.
- Error uniforme: `{ "error": "mensaje" }`.
- JWT: header `Authorization: Bearer <access_token>`.
- HTML de noticias se sanitiza en servidor (`nh3`), no se confía en TipTap.
- Subidas: tipos `pdf/jpg/png`, tope **20 MB**.

---

## Revisión de la propuesta original de la IA

La primera generación de OpenAPI (típica de un LLM sin el código) se revisó línea por línea.

### 1. Métodos HTTP

| Propuesta IA | Problema | Corrección del equipo |
|---|---|---|
| `GET /api/auth/login?email=&password=` | Credenciales en query string (logs, historial) | **`POST` + body JSON** |
| `POST /api/news/{id}` para actualizar | No idiomático REST | **`PUT /api/news/{id}`** (reemplazo de recurso, como el Flask actual) |
| `GET /api/newspapers/upload` | Get no debe crear archivos | **`POST` multipart** |
| Endpoint `POST /api/radio/mute` | El servidor no controla el altavoz del navegador | **Eliminado.** El interlock TV/Radio es estado Pinia en la SPA |

### 2. Códigos de respuesta

| Propuesta IA | Problema | Corrección |
|---|---|---|
| `200` al crear noticia/usuario/programa | El cliente no distingue creación | **`201 Created`** |
| `401` cuando el correo no es `@upec.edu.ec` | Confunde “no autenticado” con “prohibido” | **`403 Forbidden`** + mensaje de dominio |
| `401` cuando el rol no alcanza | Igual confusión | **`403`** `Acceso denegado: permisos insuficientes` |
| `500` si Icecast cae | El portal público no debe romperse | **`200` con fallback** (`title: Desconocido`, `listeners: 0`) |
| Sin `404` en detalle por slug | OpenAPI incompleto | **`404`** documentado |

### 3. Payloads

| Propuesta IA | Problema | Corrección |
|---|---|---|
| Login `{username, password}` | El requisito es identidad institucional por **email** | `{email, password}` |
| Periódico JSON `{pdf_base64: ...}` | Payload enorme, sin validar magic bytes | `multipart/form-data` (`file`, `title`, `publication_date`) |
| Programa `{docentes: "Ana, Luis"}` | String no consultable | Arrays `teachers[]`, `students[]`, `projects[]` |
| YouTube `{apiKey}` en el cliente | Filtración del secreto | Solo query `limit`; la key vive en el servidor |
| Noticia sin `status` | No hay borrador | `draft \| published \| archived` |

### 4. Manejo de errores

| Propuesta IA | Problema | Corrección |
|---|---|---|
| `{message: "..."}` o `{detail: "..."}` mezclados | Cliente SPA tendría dos parsers | Estándar `{error: string}` |
| HTML de error Flask por defecto | Rompe Axios | JSON en todos los blueprints |
| 422 FastAPI `ValidationError` | No usamos FastAPI | 400 con mensaje explícito |

---

## Ejemplo de payloads (contrato final)

**Login**

```http
POST /api/auth/login
Content-Type: application/json

{"email":"editor@upec.edu.ec","password":"********"}
```

```json
{
  "access_token": "<jwt>",
  "refresh_token": "<jwt>",
  "user": {
    "id": 2,
    "username": "editor",
    "email": "editor@upec.edu.ec",
    "is_active": true,
    "roles": ["editor"]
  }
}
```

**Crear noticia**

```http
POST /api/news
Authorization: Bearer <jwt>
Content-Type: application/json

{
  "title": "UPEC inaugura estudio de TV",
  "content_html": "<p>Texto</p>",
  "excerpt": "Resumen",
  "status": "published",
  "category_ids": [1]
}
```

Respuesta **201** con `slug` generado y `author` tomado del JWT (no del body: la IA permitía falsificar `author_id`).

---

## Seguridad del contrato (revisión humana)

- No hay verbos inseguros en recursos públicos de escritura.
- Rate limiting / CORS se configuran en despliegue (`CORS_ORIGINS`); no van en el JSON de negocio.
- `/api/users` es **solo SuperAdmin**.
- Logout añade el `jti` a blocklist (en producción conviene Redis; en local es set en memoria — la IA lo omitió).

---

## Matriz RBAC (roles × operaciones)

La IA puso “admin puede todo” en un solo rol `admin`. Se partió en tres roles del requisito:

| Recurso | Público | Editor | Gestor programas | SuperAdmin |
|---|---|---|---|---|
| `GET` noticias/programas/periódicos/YouTube/radio | sí | sí | sí | sí |
| `POST/PUT` `/api/news`, `/api/newspapers` | no | sí | no | sí |
| `DELETE` `/api/news/{id}` (archiva) | no | sí | no | sí |
| `DELETE` `/api/newspapers/{id}` (borra fila) | no | sí | no | sí |
| `POST/PUT/DELETE` `/api/programs` | no | no | sí | sí |
| `GET/POST/PUT/DELETE` `/api/users` | no | no | no | sí |
| `POST` `/api/uploads/*` | no | JWT (cualquier rol staff) | JWT | JWT |
| `POST` `/api/auth/login` | sí (filtro dominio) | — | — | — |

`DELETE` de noticia, usuario y programa en el código **no es borrado físico**: noticia → `archived`, usuario → `is_active=false`, programa → `is_active=false`. El periódico sí se elimina de BD. Eso se corrigió en OpenAPI (la IA había puesto 204 No Content y borrado duro en todos).

---

## Catálogo de códigos HTTP usados de verdad

| Código | Cuándo |
|---|---|
| 200 | Lectura, update, logout, archivo lógico, radio fallback |
| 201 | Alta de noticia, usuario, programa, periódico, upload |
| 400 | Body incompleto, PDF inválido, email duplicado, fecha malformada |
| 401 | Sin JWT, JWT inválido, password incorrecto |
| 403 | Dominio no UPEC, usuario inactivo, rol insuficiente |
| 404 | Slug o id inexistente (`first_or_404` / `get_or_404`) |
| 500 | YouTube sin API Key/playlist y sin caché previa |

No se usa 204 porque Flask siempre devuelve JSON `{message}` o el recurso. No se usa 422 porque no hay capa Pydantic.

---

## Cómo visualizar / entregar al docente

1. Abrir [`openapi.yaml`](./openapi.yaml) en [Swagger Editor](https://editor.swagger.io) o Redoc.
2. Exportar PDF desde el editor **o** incluir este Markdown + YAML en el documento de equipo (entregable 2 de la práctica: diagramas + OpenAPI).
3. Los diagramas C4/ER de `01` y `02` se pueden pegar en Draw.io (Arrange → Insert → Advanced → Mermaid).
