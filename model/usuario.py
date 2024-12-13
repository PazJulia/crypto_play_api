from sqlalchemy import Column, Integer, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from model import Base

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    saldo_disponivel = Column(Float, default=500.0)  # Valor inicial padrão
    balanco_total = Column(Float, default=0.0)
    data_criacao = Column(DateTime, default=datetime.now())

    moedas = relationship("Moeda", backref="usuario")

    __table_args__ = (UniqueConstraint('id', name='unique_usuario'),)