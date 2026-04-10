from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import get_db
from schemas import DensidadRequest
from service import calcular_densidad

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"mensaje": "API densidad funcionando"}

@app.post("/calcular-densidad")
def calcular(data: DensidadRequest, db: Session = Depends(get_db)):
    resultado = calcular_densidad(db, data.api, data.temperatura)

    if not resultado:
        return {"error": "No se pudo calcular"}

    return resultado
