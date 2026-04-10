from pydantic import BaseModel

class DensidadRequest(BaseModel):
    api: float
    temperatura: float
