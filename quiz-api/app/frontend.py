from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/ui/", include_in_schema=False)
def ui_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/ui/preguntas", include_in_schema=False)
def ui_preguntas(request: Request):
    return templates.TemplateResponse("preguntas.html", {"request": request})


@router.get("/ui/sesiones", include_in_schema=False)
def ui_sesiones(request: Request):
    return templates.TemplateResponse("sesiones.html", {"request": request})


@router.get("/ui/estadisticas", include_in_schema=False)
def ui_estadisticas(request: Request):
    return templates.TemplateResponse("estadisticas.html", {"request": request})


@router.get("/ui/quiz", include_in_schema=False)
def ui_quiz(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})
