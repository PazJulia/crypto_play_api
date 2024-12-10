from flask_openapi3 import Schema
from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base

class Moeda(Base):
    __tablename__ = 'moeda'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    coin_gecko_id = Column(String)
    valor_comprado_brl = Column(Float)
    data_inseracao = Column(DateTime, default=datetime.now())

    def __init__(self, nome:str, coin_gecko_id:str, valor_comprado_brl:Float, data_insercao:Union[DateTime, None] = None):
        self.nome = nome
        self.coin_gecko_id = coin_gecko_id
        self.valor_comprado_brl = valor_comprado_brl

        if (data_insercao):
            self.data_inseracao = data_insercao


class MoedaSchema(Schema):
    nome: str = ""
    coin_gecko_id: str = ""
    valor_comprado_brl: float = ""