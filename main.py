from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import get_db
from schemas import DensidadRequest
from service import calcular_densidad


app = FastAPI()


# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# RUTA PRINCIPAL
# =========================
@app.get("/")
def home():
    return {
        "mensaje": "API densidad funcionando"
    }


# =========================
# CALCULAR DENSIDAD
# =========================
@app.post("/calcular-densidad")
def calcular(
    data: DensidadRequest,
    db: Session = Depends(get_db)
):
    try:

        print("====================================")
        print("SOLICITUD RECIBIDA")
        print("API:", data.api)
        print("TEMPERATURA:", data.temperatura)
        print("====================================")

        resultado = calcular_densidad(
            db,
            data.api,
            data.temperatura
        )

        if not resultado:
            print("No se pudo calcular la densidad")
            return {
                "error": "No se pudo calcular"
            }

        print("RESULTADO:", resultado)

        return resultado

    except Exception as e:

        print("====================================")
        print("ERROR EN CALCULAR DENSIDAD")
        print("TIPO:", type(e).__name__)
        print("ERROR:", str(e))
        print("====================================")

        raise