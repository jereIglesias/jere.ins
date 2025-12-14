from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from .. import services, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/preguntas", tags=["preguntas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.PreguntaRead, status_code=status.HTTP_201_CREATED)
def crear_pregunta(p: schemas.PreguntaCreate, db: Session = Depends(get_db)):
    return services.crear_pregunta(db, p)


@router.get("/", response_model=list[schemas.PreguntaRead])
def listar_preguntas(skip: int = 0, limit: int = 20, categoria: str | None = Query(None), db: Session = Depends(get_db)):
    return services.listar_preguntas(db, skip=skip, limit=limit, categoria=categoria)


@router.get("/aleatorias", response_model=list[schemas.PreguntaRead])
def preguntas_aleatorias(cantidad: int = 10, categoria: str | None = Query(None), db: Session = Depends(get_db)):
    return services.preguntas_aleatorias(db, cantidad, categoria)


@router.get("/{pregunta_id}", response_model=schemas.PreguntaRead)
def get_pregunta(pregunta_id: int, db: Session = Depends(get_db)):
    return services.obtener_pregunta(db, pregunta_id)


@router.put("/{pregunta_id}", response_model=schemas.PreguntaRead)
def update_pregunta(pregunta_id: int, p: schemas.PreguntaCreate, db: Session = Depends(get_db)):
    return services.actualizar_pregunta(db, pregunta_id, p)


@router.delete("/{pregunta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pregunta(pregunta_id: int, db: Session = Depends(get_db)):
    services.borrar_pregunta(db, pregunta_id)
    return {}
