# PARTE 2 — Diseño del sistema (2.0 pts)

Portal institucional y CMS a medida **UPEC / Canales Digitales**.

| Stack | Uso |
|---|---|
| **Node.js** (Vue 3 + Vite + Pinia) | SPA pública y panel CMS |
| **Python 3.12** (Flask + Gunicorn) | API REST |
| **MySQL 8** | Persistencia institucional |

## Artefactos (un líder por archivo según la práctica)

| Archivo | Sección | Contenido |
|---|---|---|
| [01-arquitectura.md](./01-arquitectura.md) | 2.1 | C4 contexto + contenedores, componentes, decisiones, bitácora IA |
| [02-modelo-datos.md](./02-modelo-datos.md) | 2.2 | ER, evaluación 3FN, correcciones a la IA |
| [schema.sql](./schema.sql) | 2.2 | DDL MySQL 8 final |
| [03-api-rest.md](./03-api-rest.md) | 2.3 | Revisión HTTP/códigos/payloads vs. propuesta IA |
| [openapi.yaml](./openapi.yaml) | 2.3 | OpenAPI 3.0 (≥ 5 endpoints; contrato completo) |

Herramienta de IA de esta fase: **Cursor** (diseño a partir de requisitos REQ/RF y del repositorio).  
Prompts y correcciones humanas están **dentro de cada documento** (la rúbrica pide evidencia de uso crítico de IA, no copiar el primer output).

## Autoevaluación rúbrica Parte 2 (completitud y coherencia)

| Criterio de la práctica | Dónde está cubierto |
|---|---|
| C4 Nivel 1 Contexto y Nivel 2 Contenedores | `01` — diagramas Mermaid C4 |
| Componentes, responsabilidades e interfaces | `01` — tablas + C4 Nivel 3 del API |
| Justificación de decisiones con IA | `01` — tabla de decisiones y rechazos |
| Cómo ayudó la IA y qué se corrigió | `01`, `02` y `03` (bitácoras) |
| ER generado, evaluación 3FN, entidades faltantes | `02` |
| DDL final | `schema.sql` |
| OpenAPI ≥ 5 endpoints | `openapi.yaml` (auth, news, programs, newspapers, youtube, radio, users, uploads) |
| Revisión de verbos, códigos, payloads y errores | `03` |
| Cambios sobre la propuesta IA | `03` — tablas 1 a 4 + matriz RBAC |
| Stack pedido (Node.js + Python 3.12) | `01` y este README |

## Cómo presentarlo (2–3 min de tu parte)

1. Contexto C4: actores UPEC + YouTube + Icecast.  
2. Contenedores: SPA Node.js no recarga (radio), API Python 3.12, MySQL.  
3. Rechazo explícito: WordPress, MongoDB, API Key en el front, `POST /radio/mute`.  
4. ER: de 3 tablas planas a 3FN.  
5. Swagger: login 403 de dominio, 201 al crear, multipart PDF.

Exportar: Mermaid → Draw.io; YAML → [editor.swagger.io](https://editor.swagger.io) → PDF.
