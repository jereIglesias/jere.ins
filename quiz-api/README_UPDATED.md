# 📝 Proyecto Final: Quiz Interactivo (FastAPI + SQLAlchemy + SQLite)

Este repositorio contiene una API REST para un quiz interactivo implementada con FastAPI, SQLAlchemy y SQLite. Incluye un frontend simple servido desde la misma aplicación (`/ui/`) y documentación automática en `/docs`.

## Quick start

Requisitos: Python 3.8+ y un entorno virtual.

1. Abrir PowerShell en la carpeta del proyecto:

```powershell
cd 'C:\Users\estudiante\Desktop\EndgameApp\quiz-api'
```

2. Activar el entorno virtual (Windows PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Instalar dependencias (si no están instaladas):

```powershell
pip install -r requirements.txt
```

4. Iniciar el servidor (desarrollo):

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

la api esta disponible en: `http://127.0.0.1:8000`

La documentación interactiva en: `http://127.0.0.1:8000/docs`

El frontend en: `http://127.0.0.1:8000/ui/`

## Endpoints principales

- `GET  /questions/` : listar preguntas (soporta `skip`, `limit`, y filtro `categoria`)
- `POST /questions/` : crear pregunta
- `GET  /questions/{id}` : obtener pregunta por ID
- `GET  /questions/random?limit=N` : obtener N preguntas aleatorias
- `PUT  /questions/{id}` : actualizar pregunta
- `DELETE /questions/{id}` : soft-delete (marca `is_active=False`)
- `POST /questions/bulk` : crear preguntas en bloque
- `POST /quiz-sessions/` : iniciar sesión de quiz
- `GET  /quiz-sessions/` : listar sesiones (paginación: `skip`, `limit`)
- `GET  /quiz-sessions/{id}` : obtener sesión
- `PUT  /quiz-sessions/{id}/complete` : finalizar sesión (calcula y persiste puntuación)
- `DELETE /quiz-sessions/{id}` : eliminar sesión
- `POST /answers/` : registrar respuesta (previene duplicados por sesión/pregunta)
- `GET  /answers/session/{session_id}` : respuestas de una sesión
- `GET  /answers/{id}` : obtener respuesta específica
- `GET  /statistics/global` : estadísticas globales
- `GET  /statistics/session/{session_id}` : estadísticas de una sesión
- `GET  /statistics/questions/difficult` : preguntas ordenadas por tasa de error
- `GET  /statistics/categories` : rendimiento por categoría

## Ejemplos de uso

```powershell
# Preguntas aleatorias
curl "http://127.0.0.1:8000/questions/random?limit=5"

# Crear sesión
curl -X POST "http://127.0.0.1:8000/quiz-sessions/" -H "Content-Type: application/json" -d '{"usuario_nombre":"Estudiante"}'

# Registrar respuesta
curl -X POST "http://127.0.0.1:8000/answers/" -H "Content-Type: application/json" -d '{"sesion_id":1,"pregunta_id":3,"opcion_seleccionada":2,"tiempo_respuesta_segundos":8}'

# Finalizar sesión
curl -X PUT "http://127.0.0.1:8000/quiz-sessions/1/complete"

# Estadísticas globales
curl "http://127.0.0.1:8000/statistics/global"
```


- Swagger UI: `http://127.0.0.1:8000/docs` — usar para probar los endpoints interactivamente.


- Endpoints CRUD para preguntas, sesiones y respuestas (español + router en inglés `api_v1`).
- Modelos SQLAlchemy actualizados (`Pregunta`, `SesionQuiz`, `Respuesta`) con campos requeridos (`explicacion`, `dificultad`, `is_active`, métricas de sesión, `tiempo_respuesta_segundos`).
- Validaciones Pydantic: `opciones` 3–5, `respuesta_correcta` dentro de rango, `dificultad` restringida.
- Servicios: lógica de negocio para preguntas aleatorias, soft-delete, prevención de respuestas duplicadas, finalización de sesión con cálculo de métricas, bulk-create y estadísticas.
- Seed: ~21 preguntas añadidas. (Nota: seed recrea BD si detecta esquema incompatible — ver advertencia arriba.)
- Frontend simple en `app/static/` (`main.js`, `styles.css`) y plantillas Jinja2 bajo `app/templates/`.