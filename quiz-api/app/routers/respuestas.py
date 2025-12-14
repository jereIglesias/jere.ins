from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import services, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/respuestas", tags=["respuestas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.RespuestaRead, status_code=status.HTTP_201_CREATED)
def crear_respuesta(r: schemas.RespuestaCreate, db: Session = Depends(get_db)):
    return services.crear_respuesta(db, r)


@router.get("/sesion/{sesion_id}", response_model=list[schemas.RespuestaRead])
def listar_por_sesion(sesion_id:int, db: Session = Depends(get_db)):
    return services.listar_respuestas_por_sesion(db, sesion_id)
