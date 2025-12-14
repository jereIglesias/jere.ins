from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


ALLOWED_DIFICULTADES = {"fácil", "medio", "difícil"}


class PreguntaCreate(BaseModel):
    enunciado: str = Field(..., min_length=1)
    opciones: List[str] = Field(..., min_items=3, max_items=5)
    respuesta_correcta: int
    explicacion: Optional[str] = None
    categoria: Optional[str] = None
    dificultad: Optional[str] = None

    @validator("dificultad")
    def validar_dificultad(cls, v):
        if v is None:
            return v
        if v not in ALLOWED_DIFICULTADES:
            raise ValueError(f"dificultad debe ser una de {ALLOWED_DIFICULTADES}")
        return v

    @validator("respuesta_correcta")
    def check_correct_in_range(cls, v, values):
        opciones = values.get("opciones")
        if opciones is None:
            raise ValueError("Se requieren opciones para validar respuesta_correcta")
        if not (0 <= v < len(opciones)):
            raise ValueError("respuesta_correcta debe ser un índice válido dentro de opciones")
        return v


class PreguntaRead(BaseModel):
    id: int
    enunciado: str
    opciones: List[str]
    respuesta_correcta: int
    explicacion: Optional[str]
    categoria: Optional[str]
    dificultad: Optional[str]
    is_active: bool
    creada_en: datetime

    class Config:
        orm_mode = True


class SesionCreate(BaseModel):
    usuario_nombre: Optional[str] = None
    pregunta_ids: Optional[List[int]] = None  # si se quiere inicial con preguntas concretas
    cantidad_aleatoria: Optional[int] = None  # pedir N preguntas aleatorias


class SesionRead(BaseModel):
    id: int
    usuario_nombre: Optional[str]
    creada_en: datetime
    finalizada_en: Optional[datetime]
    completada: bool
    puntuacion_total: int
    preguntas_respondidas: int
    preguntas_correctas: int
    estado: str
    tiempo_total_segundos: Optional[int]

    class Config:
        orm_mode = True


class RespuestaCreate(BaseModel):
    sesion_id: int
    pregunta_id: int
    opcion_seleccionada: int
    tiempo_respuesta_segundos: Optional[int] = None


class RespuestaRead(BaseModel):
    id: int
    sesion_id: int
    pregunta_id: int
    opcion_seleccionada: int
    correcta: bool
    tiempo_respuesta_segundos: Optional[int]
    respondida_en: datetime

    class Config:
        orm_mode = True
