from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from .database import engine, Base
from .routers import preguntas, sesiones, respuestas
from .routers import api_v1
from . import seed_data
from sqlalchemy import func
from .frontend import router as frontend_router

app = FastAPI(title="Quiz API - Final")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", include_in_schema=False)
def root_index():
    return RedirectResponse(url="/ui/")

# crear tablas
Base.metadata.create_all(bind=engine)

# incluir routers API
app.include_router(preguntas.router)
app.include_router(sesiones.router)
app.include_router(respuestas.router)
app.include_router(api_v1.router)

# Include frontend router (TemplateResponse for /ui/ routes)
app.include_router(frontend_router)

# endpoint de estadísticas
@app.get("/estadisticas/global")
def estadisticas_global():
    from .database import SessionLocal
    from .models import Pregunta, SesionQuiz, Respuesta
    db = SessionLocal()
    try:
        total_preg = db.query(Pregunta).count()
        por_categoria = {}
        for row in db.query(Pregunta.categoria, func.count(Pregunta.id)).group_by(Pregunta.categoria):
            cat, cnt = row
            por_categoria[cat or "sin_categoria"] = cnt
        total_sesiones = db.query(SesionQuiz).count()
        total_respuestas = db.query(Respuesta).count()
        promedio_respuestas_por_sesion = (total_respuestas / total_sesiones) if total_sesiones else 0
        return {
            "total_preguntas": total_preg,
            "por_categoria": por_categoria,
            "total_sesiones": total_sesiones,
            "total_respuestas": total_respuestas,
            "promedio_respuestas_por_sesion": promedio_respuestas_por_sesion
        }
    finally:
        db.close()

# endpoint estadisticas por sesión
@app.get("/estadisticas/sesion/{sesion_id}")
def estadisticas_por_sesion(sesion_id:int):
    from .database import SessionLocal
    from .models import SesionQuiz, Respuesta
    from fastapi import HTTPException
    db = SessionLocal()
    try:
        s = db.query(SesionQuiz).filter(SesionQuiz.id == sesion_id).first()
        if not s:
            raise HTTPException(status_code=404, detail="Sesión no encontrada")
        total = len(s.respuestas)
        correctas = sum(1 for r in s.respuestas if r.correcta)
        porcentaje = (correctas/total*100) if total>0 else 0
        return {
            "sesion_id": s.id,
            "usuario_nombre": s.usuario_nombre,
            "total_respuestas": total,
            "correctas": correctas,
            "porcentaje": porcentaje,
            "finalizada": s.completada
        }
    finally:
        db.close()

# añadir seed inicial al arrancar si la DB está vacía
@app.on_event("startup")
def startup_event():
    seed_data.seed_if_empty()
