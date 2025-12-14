from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import services, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/sesiones", tags=["sesiones"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.SesionRead, status_code=status.HTTP_201_CREATED)
def crear_sesion(s: schemas.SesionCreate, db: Session = Depends(get_db)):
    return services.crear_sesion(db, s)


@router.get("/{sesion_id}", response_model=schemas.SesionRead)
def get_sesion(sesion_id:int, db: Session = Depends(get_db)):
    return services.obtener_sesion(db, sesion_id)


@router.post("/{sesion_id}/finalizar")
def finalizar_sesion(sesion_id:int, db: Session = Depends(get_db)):
    return services.finalizar_sesion(db, sesion_id)
