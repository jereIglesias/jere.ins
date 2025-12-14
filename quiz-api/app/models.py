from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Index, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Pregunta(Base):
    __tablename__ = "preguntas"
    id = Column(Integer, primary_key=True, index=True)
    enunciado = Column(String, nullable=False)
    opciones = Column(JSON, nullable=False)  # lista de strings
    respuesta_correcta = Column(Integer, nullable=False)  # índice en opciones (0-based)
    explicacion = Column(Text, nullable=True)
    categoria = Column(String, index=True, nullable=True)
    dificultad = Column(String, nullable=True)  # 'fácil','medio','difícil'
    is_active = Column(Boolean, default=True, index=True)
    creada_en = Column(DateTime, default=datetime.utcnow, index=True)

    respuestas = relationship("Respuesta", back_populates="pregunta", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_pregunta_categoria", "categoria"),
    )


class SesionQuiz(Base):
    __tablename__ = "sesiones"
    id = Column(Integer, primary_key=True, index=True)
    usuario_nombre = Column(String, nullable=True)
    creada_en = Column(DateTime, default=datetime.utcnow)
    finalizada_en = Column(DateTime, nullable=True)
    completada = Column(Boolean, default=False)
    puntuacion_total = Column(Integer, default=0)
    preguntas_respondidas = Column(Integer, default=0)
    preguntas_correctas = Column(Integer, default=0)
    estado = Column(String, default="en_progreso")
    tiempo_total_segundos = Column(Integer, nullable=True)

    respuestas = relationship("Respuesta", back_populates="sesion", cascade="all, delete-orphan")


class Respuesta(Base):
    __tablename__ = "respuestas"
    id = Column(Integer, primary_key=True, index=True)
    sesion_id = Column(Integer, ForeignKey("sesiones.id"), nullable=False, index=True)
    pregunta_id = Column(Integer, ForeignKey("preguntas.id"), nullable=False, index=True)
    opcion_seleccionada = Column(Integer, nullable=False)  # índice 0-based
    correcta = Column(Boolean, nullable=False)
    tiempo_respuesta_segundos = Column(Integer, nullable=True)
    respondida_en = Column(DateTime, default=datetime.utcnow)

    sesion = relationship("SesionQuiz", back_populates="respuestas")
    pregunta = relationship("Pregunta", back_populates="respuestas")

    __table_args__ = (
        UniqueConstraint('sesion_id', 'pregunta_id', name='uix_sesion_pregunta'),
    )
