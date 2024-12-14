from flask_openapi3 import Schema
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from datetime import datetime
from typing import Union

from model import Base

class Moeda(Base):
    __tablename__ = 'moeda'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    coin_gecko_id = Column(String)
    cota = Column(Float)
    simbolo_url = Column(String)
    data_inseracao = Column(DateTime, default=datetime.now())
    usuario_id = Column(Integer, ForeignKey('usuario.id'))  # Relacionamento com o usuário

def __init__(self, nome:str, coin_gecko_id:str, cota:Float, simbolo_url:str, usuario_id: int, data_insercao:Union[DateTime, None] = None):
        self.nome = nome
        self.coin_gecko_id = coin_gecko_id
        self.cota = cota
        self.simbolo_url = simbolo_url
        self.usuario_id = usuario_id

        if (data_insercao):
            self.data_inseracao = data_insercao


class MoedaSchema(Schema):
    nome: str = ""
    coin_gecko_id: str = ""
    cota: float = ""
    simbolo_url: str = ""
