# Guía de Contribución - Mindalae RadioTV (UPEC)

¡Gracias por contribuir al CMS Institucional! Para mantener la calidad del código, utilizamos asistencia de IA (GitHub Copilot / Claude) y revisiones humanas. Sigue estos estándares:

## 1. Estrategia de Ramas (GitHub Flow)
- La rama `main` está protegida.
- Para nuevas funcionalidades, crea una rama: `feature/nombre-funcionalidad`.
- Para errores, crea una rama: `bugfix/nombre-error`.

## 2. Estándares de Código
- **Backend (Python/Flask):** Sigue la guía de estilo PEP-8. Usa `snake_case` para variables y funciones. Las clases deben usar `PascalCase`.
- **Frontend (Vue/Tailwind):** Los componentes deben usar `PascalCase` (ej. `RadioPlayer.vue`). Utiliza los colores institucionales: Verde UPEC (`#006633`) y Amarillo (`#FFCE00`).

## 3. Uso de IA en el Desarrollo
- Es obligatorio auditar el código generado por IA (Copilot/ChatGPT) antes de hacer un commit.
- Asegúrate de no subir contraseñas, API Keys o JWT secrets en los prompts de IA.

## 4. Pull Requests (PR)
- Todo código debe pasar por un PR y ser aprobado por al menos 1 revisor humano.
- El pipeline CI/CD (`deploy.yml`) ejecutará `pytest` automáticamente. El PR no se puede fusionar si las pruebas fallan.
