from .database import SessionLocal, engine, Base
from .models import Pregunta, SesionQuiz, Respuesta
from sqlalchemy.exc import OperationalError
import os
from datetime import datetime, timedelta
import random


def seed_if_empty():
    db = SessionLocal()
    try:
        try:
            total = db.query(Pregunta).count()
        except OperationalError:
            # DB schema is out-of-date (column missing). Remove DB file and recreate schema.
            try:
                db_path = engine.url.database
                db.close()
                # Dispose engine connections before removing file
                try:
                    engine.dispose()
                except Exception:
                    pass
                # Use absolute path to be safe
                if db_path:
                    abs_path = os.path.abspath(db_path)
                    if os.path.exists(abs_path):
                        os.remove(abs_path)
            except Exception:
                pass

            Base.metadata.create_all(bind=engine)
            db = SessionLocal()
            total = db.query(Pregunta).count()

        if total >= 20:
            return

        preguntas = [
            Pregunta(
                enunciado="¿Qué framework se utiliza en este proyecto para crear la API?",
                opciones=["Django", "Flask", "FastAPI", "Tornado"],
                respuesta_correcta=2,
                categoria="Tecnologías",
                dificultad="fácil"
            ),
            Pregunta(
                enunciado="¿Qué servidor ASGI se sugiere en `requirements.txt` para ejecutar la app?",
                opciones=["gunicorn", "uvicorn", "waitress", "daphne"],
                respuesta_correcta=1,
                categoria="DevOps",
                dificultad="fácil"
            ),
            Pregunta(
                enunciado="En este proyecto, ¿qué motor se usa para mapear modelos a la base de datos?",
                opciones=["Django ORM", "Peewee", "SQLAlchemy", "PonyORM"],
                respuesta_correcta=2,
                categoria="Tecnologías",
                dificultad="medio"
            ),
            Pregunta(
                enunciado="¿Qué librería se utiliza para renderizar plantillas HTML en el backend?",
                opciones=["Mako", "Jinja2", "Chameleon", "Mustache"],
                respuesta_correcta=1,
                categoria="Tecnologías",
                dificultad="fácil"
            ),
            Pregunta(
                enunciado="¿Cuál es la ruta estática donde están `main.js` y `styles.css`?",
                opciones=["/static/", "/assets/", "/public/", "/ui/static/"],
                respuesta_correcta=0,
                categoria="Arquitectura",
                dificultad="fácil"
            ),
            Pregunta(
                enunciado="En REST, ¿qué método HTTP se usa típicamente para crear un recurso?",
                opciones=["GET", "POST", "PUT", "DELETE"],
                respuesta_correcta=1,
                categoria="HTTP",
                dificultad="fácil"
            ),
            Pregunta(
                enunciado="¿Qué archivo contiene las dependencias Python del proyecto?",
                opciones=["Pipfile", "requirements.txt", "pyproject.toml", "setup.cfg"],
                respuesta_correcta=1,
                categoria="DevOps",
                dificultad="fácil"
            ),
            Pregunta(
                enunciado="¿Cómo se llama la función usada para crear tablas en SQLAlchemy?",
                opciones=["create_tables()", "Base.create_all()", "Base.metadata.create_all()", "engine.create_all()"],
                respuesta_correcta=2,
                categoria="SQLAlchemy",
                dificultad="medio"
            ),
            Pregunta(
                enunciado="¿Qué tipo de respuesta utiliza FastAPI para devolver plantillas Jinja2?",
                opciones=["JSONResponse", "FileResponse", "TemplateResponse", "HTMLResponse"],
                respuesta_correcta=2,
                categoria="FastAPI",
                dificultad="medio"
            ),
            Pregunta(
                enunciado="¿Qué comando inicia la aplicación con recarga automática?",
                opciones=["python app/main.py", "uvicorn app.main:app --reload", "flask run --reload", "gunicorn app.main:app"],
                respuesta_correcta=1,
                categoria="DevOps",
                dificultad="fácil"
            ),
            Pregunta(
                enunciado="¿Dónde está el código cliente (JS y CSS) del proyecto?",
                opciones=["app/static/", "app/templates/", "data/", "app/routers/"],
                respuesta_correcta=0,
                categoria="Arquitectura",
                dificultad="fácil"
            ),
            Pregunta(
                enunciado="¿Qué extensión usan las plantillas HTML con Jinja2?",
                opciones=[".jinja", ".tpl", ".html", ".j2"],
                respuesta_correcta=2,
                categoria="Tecnologías",
                dificultad="fácil"
            ),
            Pregunta(
                enunciado="¿Cuál es la URL para acceder al quiz interactivo?",
                opciones=["/quiz", "/ui/quiz", "/play", "/test"],
                respuesta_correcta=1,
                categoria="Arquitectura",
                dificultad="fácil"
            ),
            Pregunta(
                enunciado="¿Qué método HTTP se usa para obtener datos sin modificar?",
                opciones=["GET", "POST", "PUT", "DELETE"],
                respuesta_correcta=0,
                categoria="HTTP",
                dificultad="fácil"
            ),
            Pregunta(
                enunciado="¿Cuál es el puerto en el que corre la aplicación?",
                opciones=["3000", "5000", "8000", "8080"],
                respuesta_correcta=2,
                categoria="DevOps",
                dificultad="fácil"
            ),
            Pregunta(
                enunciado="¿Qué base de datos se utiliza en el proyecto?",
                opciones=["PostgreSQL", "MySQL", "SQLite", "MongoDB"],
                respuesta_correcta=2,
                categoria="Bases de Datos",
                dificultad="fácil"
            ),
            Pregunta(
                enunciado="¿Qué carpeta contiene los routers de las rutas de la API?",
                opciones=["app/api/", "app/routes/", "app/routers/", "routers/"],
                respuesta_correcta=2,
                categoria="Arquitectura",
                dificultad="fácil"
            ),
            Pregunta(
                enunciado="¿Cuál es el principal archivo de entrada de la aplicación?",
                opciones=["main.py", "app.py", "run.py", "server.py"],
                respuesta_correcta=0,
                categoria="Arquitectura",
                dificultad="fácil"
            ),
            Pregunta(
                enunciado="¿Qué modelo almacena las preguntas del quiz?",
                opciones=["Question", "Pregunta", "Quiz", "Answer"],
                respuesta_correcta=1,
                categoria="Modelos",
                dificultad="fácil"
            ),
            Pregunta(
                enunciado="¿Qué tipo de validación usa FastAPI por defecto?",
                opciones=["Schema", "Pydantic", "Marshmallow", "Cerberus"],
                respuesta_correcta=1,
                categoria="FastAPI",
                dificultad="medio"
            ),
            Pregunta(
                enunciado="¿Dónde se guardan las sesiones del quiz?",
                opciones=["/data/", "/sessions/", "En la base de datos", "/cache/"],
                respuesta_correcta=2,
                categoria="Bases de Datos",
                dificultad="fácil"
            ),
        ]
        
        for p in preguntas:
            existing = db.query(Pregunta).filter_by(enunciado=p.enunciado).first()
            if not existing:
                db.add(p)
        
        db.commit()
    finally:
        db.close()
