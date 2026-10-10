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
