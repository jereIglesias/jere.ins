from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from fastapi import HTTPException, status
from datetime import datetime
import random

# Preguntas
def crear_pregunta(db: Session, pregunta_in: schemas.PreguntaCreate):
    p = models.Pregunta(
        enunciado=pregunta_in.enunciado,
        opciones=pregunta_in.opciones,
        respuesta_correcta=pregunta_in.respuesta_correcta,
        explicacion=getattr(pregunta_in, 'explicacion', None),
        categoria=pregunta_in.categoria,
        dificultad=pregunta_in.dificultad,
        is_active=True,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def obtener_pregunta(db: Session, pregunta_id: int):
    p = db.query(models.Pregunta).filter(models.Pregunta.id == pregunta_id).first()
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pregunta no encontrada")
    return p

def listar_preguntas(db: Session, skip: int = 0, limit: int = 20, categoria: str = None):
    q = db.query(models.Pregunta).filter(models.Pregunta.is_active == True)
    if categoria:
        q = q.filter(models.Pregunta.categoria == categoria)
    return q.offset(skip).limit(limit).all()

def actualizar_pregunta(db: Session, pregunta_id: int, update: schemas.PreguntaCreate):
    p = obtener_pregunta(db, pregunta_id)
    p.enunciado = update.enunciado
    p.opciones = update.opciones
    p.respuesta_correcta = update.respuesta_correcta
    p.categoria = update.categoria
    p.dificultad = update.dificultad
    p.explicacion = getattr(update, 'explicacion', None)
    db.commit()
    db.refresh(p)
    return p

def borrar_pregunta(db: Session, pregunta_id: int):
    p = obtener_pregunta(db, pregunta_id)
    # soft delete
    p.is_active = False
    db.commit()
    return True

def preguntas_aleatorias(db: Session, cantidad: int = 10, categoria: str = None):
    q = db.query(models.Pregunta).filter(models.Pregunta.is_active == True)
    if categoria:
        q = q.filter(models.Pregunta.categoria == categoria)
    todos = q.all()
    return random.sample(todos, k=min(cantidad, len(todos)))


# Sesiones
def crear_sesion(db: Session, sesion_in: schemas.SesionCreate):
    s = models.SesionQuiz(usuario_nombre=sesion_in.usuario_nombre)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

def obtener_sesion(db: Session, sesion_id: int):
    s = db.query(models.SesionQuiz).filter(models.SesionQuiz.id == sesion_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return s

def finalizar_sesion(db: Session, sesion_id: int):
    s = obtener_sesion(db, sesion_id)
    if s.completada:
        raise HTTPException(status_code=400, detail="Sesión ya finalizada")
    s.finalizada_en = datetime.utcnow()
    s.completada = True
    # calcular métricas
    total = len(s.respuestas)
    correctas = sum(1 for r in s.respuestas if r.correcta)
    s.preguntas_respondidas = total
    s.preguntas_correctas = correctas
    s.puntuacion_total = correctas
    s.estado = 'completado'
    # tiempo total (si hay tiempos individuales)
    tiempos = [r.tiempo_respuesta_segundos for r in s.respuestas if r.tiempo_respuesta_segundos is not None]
    s.tiempo_total_segundos = sum(tiempos) if tiempos else None
    db.commit()
    db.refresh(s)
    porcentaje = (correctas / total * 100) if total > 0 else 0
    return {"id": s.id, "total_respuestas": total, "correctas": correctas, "porcentaje": porcentaje}


# Respuestas
def crear_respuesta(db: Session, resp_in: schemas.RespuestaCreate):
    sesion = obtener_sesion(db, resp_in.sesion_id)
    pregunta = db.query(models.Pregunta).filter(models.Pregunta.id == resp_in.pregunta_id).first()
    if not pregunta:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    if resp_in.opcion_seleccionada < 0 or resp_in.opcion_seleccionada >= len(pregunta.opciones):
        raise HTTPException(status_code=400, detail="Opción seleccionada fuera de rango")
    # evitar duplicados
    exists = db.query(models.Respuesta).filter(models.Respuesta.sesion_id == resp_in.sesion_id, models.Respuesta.pregunta_id == resp_in.pregunta_id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Ya existe una respuesta para esa pregunta en esta sesión")
    correcta = (resp_in.opcion_seleccionada == pregunta.respuesta_correcta)
    r = models.Respuesta(
        sesion_id=resp_in.sesion_id,
        pregunta_id=resp_in.pregunta_id,
        opcion_seleccionada=resp_in.opcion_seleccionada,
        correcta=correcta,
        tiempo_respuesta_segundos=getattr(resp_in, 'tiempo_respuesta_segundos', None)
    )
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


def listar_respuestas_por_sesion(db: Session, sesion_id: int):
    obtener_sesion(db, sesion_id)  # valida existencia
    return db.query(models.Respuesta).filter(models.Respuesta.sesion_id == sesion_id).all()


def crear_preguntas_bulk(db: Session, preguntas_list: list[schemas.PreguntaCreate]):
    created = []
    for p_in in preguntas_list:
        p = models.Pregunta(
            enunciado=p_in.enunciado,
            opciones=p_in.opciones,
            respuesta_correcta=p_in.respuesta_correcta,
            explicacion=getattr(p_in, 'explicacion', None),
            categoria=p_in.categoria,
            dificultad=p_in.dificultad,
            is_active=True,
        )
        db.add(p)
        created.append(p)
    db.commit()
    for p in created:
        db.refresh(p)
    return created


def statistics_global(db: Session):
    # total preguntas activas
    total_preg = db.query(models.Pregunta).filter(models.Pregunta.is_active == True).count()
    por_categoria = {}
    for row in db.query(models.Pregunta.categoria, func.count(models.Pregunta.id)).group_by(models.Pregunta.categoria):
        cat, cnt = row
        por_categoria[cat or "sin_categoria"] = cnt
    total_sesiones = db.query(models.SesionQuiz).count()
    total_respuestas = db.query(models.Respuesta).count()
    promedio_respuestas_por_sesion = (total_respuestas / total_sesiones) if total_sesiones else 0
    return {
        "total_preguntas": total_preg,
        "por_categoria": por_categoria,
        "total_sesiones": total_sesiones,
        "total_respuestas": total_respuestas,
        "promedio_respuestas_por_sesion": promedio_respuestas_por_sesion
    }


def statistics_por_sesion(db: Session, sesion_id: int):
    s = db.query(models.SesionQuiz).filter(models.SesionQuiz.id == sesion_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    total = len(s.respuestas)
    correctas = sum(1 for r in s.respuestas if r.correcta)
    porcentaje = (correctas / total * 100) if total > 0 else 0
    tiempos = [r.tiempo_respuesta_segundos for r in s.respuestas if r.tiempo_respuesta_segundos is not None]
    tiempo_promedio = (sum(tiempos) / len(tiempos)) if tiempos else None
    return {
        "sesion_id": s.id,
        "usuario_nombre": s.usuario_nombre,
        "total_respuestas": total,
        "correctas": correctas,
        "porcentaje": porcentaje,
        "tiempo_promedio_segundos": tiempo_promedio,
        "finalizada": s.completada
    }


def questions_by_error_rate(db: Session, limit: int = 20):
    # calcular tasa de error por pregunta
    q = db.query(models.Pregunta).filter(models.Pregunta.is_active == True).all()
    stats = []
    for p in q:
        total = db.query(models.Respuesta).filter(models.Respuesta.pregunta_id == p.id).count()
        incorrectas = db.query(models.Respuesta).filter(models.Respuesta.pregunta_id == p.id, models.Respuesta.correcta == False).count()
        tasa_error = (incorrectas / total * 100) if total > 0 else 0
        stats.append({"pregunta_id": p.id, "enunciado": p.enunciado, "total": total, "incorrectas": incorrectas, "tasa_error": tasa_error})
    stats.sort(key=lambda x: x["tasa_error"], reverse=True)
    return stats[:limit]


def statistics_by_category(db: Session):
    cats = db.query(models.Pregunta.categoria).distinct().all()
    result = {}
    for (cat,) in cats:
        cat_name = cat or "sin_categoria"
        preguntas = db.query(models.Pregunta).filter(models.Pregunta.categoria == cat, models.Pregunta.is_active == True).all()
        total_p = len(preguntas)
        # calcular performance por categoria
        respuestas_tot = 0
        correctas = 0
        for p in preguntas:
            tot = db.query(models.Respuesta).filter(models.Respuesta.pregunta_id == p.id).count()
            corr = db.query(models.Respuesta).filter(models.Respuesta.pregunta_id == p.id, models.Respuesta.correcta == True).count()
            respuestas_tot += tot
            correctas += corr
        rendimiento = (correctas / respuestas_tot * 100) if respuestas_tot > 0 else None
        result[cat_name] = {"preguntas": total_p, "respuestas_totales": respuestas_tot, "rendimiento_porcentaje": rendimiento}
    return result
