from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import services, schemas

router = APIRouter(prefix="", tags=["api"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Questions (English endpoints matching exam)
@router.post("/questions/", response_model=schemas.PreguntaRead, status_code=status.HTTP_201_CREATED)
def create_question(payload: schemas.PreguntaCreate, db: Session = Depends(get_db)):
    return services.crear_pregunta(db, payload)


@router.get("/questions/", response_model=list[schemas.PreguntaRead])
def list_questions(skip: int = 0, limit: int = 20, categoria: str | None = Query(None), db: Session = Depends(get_db)):
    return services.listar_preguntas(db, skip=skip, limit=limit, categoria=categoria)


@router.get("/questions/random", response_model=list[schemas.PreguntaRead])
def questions_random(limit: int = 10, categoria: str | None = Query(None), db: Session = Depends(get_db)):
    return services.preguntas_aleatorias(db, limit, categoria)


@router.get("/questions/{question_id}", response_model=schemas.PreguntaRead)
def get_question(question_id: int, db: Session = Depends(get_db)):
    return services.obtener_pregunta(db, question_id)


@router.put("/questions/{question_id}", response_model=schemas.PreguntaRead)
def update_question(question_id: int, payload: schemas.PreguntaCreate, db: Session = Depends(get_db)):
    return services.actualizar_pregunta(db, question_id, payload)


@router.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    services.borrar_pregunta(db, question_id)
    return {}


@router.post("/questions/bulk", response_model=list[schemas.PreguntaRead])
def bulk_create_questions(payload: list[schemas.PreguntaCreate], db: Session = Depends(get_db)):
    return services.crear_preguntas_bulk(db, payload)


# Quiz sessions
@router.post("/quiz-sessions/", response_model=schemas.SesionRead, status_code=status.HTTP_201_CREATED)
def create_session(s: schemas.SesionCreate, db: Session = Depends(get_db)):
    return services.crear_sesion(db, s)


@router.get("/quiz-sessions/", response_model=list[schemas.SesionRead])
def list_sessions(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    q = db.query(services.models.SesionQuiz).offset(skip).limit(limit).all()
    return q


@router.get("/quiz-sessions/{session_id}", response_model=schemas.SesionRead)
def get_session(session_id: int, db: Session = Depends(get_db)):
    return services.obtener_sesion(db, session_id)


@router.put("/quiz-sessions/{session_id}/complete")
def complete_session(session_id: int, db: Session = Depends(get_db)):
    return services.finalizar_sesion(db, session_id)


@router.delete("/quiz-sessions/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    s = services.obtener_sesion(db, session_id)
    db.delete(s)
    db.commit()
    return {"ok": True}


# Answers
@router.post("/answers/", response_model=schemas.RespuestaRead, status_code=status.HTTP_201_CREATED)
def create_answer(r: schemas.RespuestaCreate, db: Session = Depends(get_db)):
    return services.crear_respuesta(db, r)


@router.get("/answers/session/{session_id}", response_model=list[schemas.RespuestaRead])
def answers_by_session(session_id: int, db: Session = Depends(get_db)):
    return services.listar_respuestas_por_sesion(db, session_id)


@router.get("/answers/{answer_id}", response_model=schemas.RespuestaRead)
def get_answer(answer_id: int, db: Session = Depends(get_db)):
    a = db.query(services.models.Respuesta).filter(services.models.Respuesta.id == answer_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Answer not found")
    return a


# Statistics
@router.get("/statistics/global")
def statistics_global(db: Session = Depends(get_db)):
    return services.statistics_global(db)


@router.get("/statistics/session/{session_id}")
def statistics_session(session_id: int, db: Session = Depends(get_db)):
    return services.statistics_por_sesion(db, session_id)


@router.get("/statistics/questions/difficult")
def questions_difficult(limit: int = 20, db: Session = Depends(get_db)):
    return services.questions_by_error_rate(db, limit)


@router.get("/statistics/categories")
def stats_by_category(db: Session = Depends(get_db)):
    return services.statistics_by_category(db)
