from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class MoedaSchema(BaseModel):
    nome: str
    coin_gecko_id: str
    cota: float
    simbolo_url: str

class UsuarioSchema(BaseModel):
    id: int
    saldo_disponivel: float
    balanco_total: float
    data_criacao: datetime
    moedas: Optional[List[MoedaSchema]] = []  # Lista de moedas associadas

    class Config:
        orm_mode = True  # Permite conversão entre objetos SQLAlchemy e Pydantic
