
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Produto(Base):
    __tablename__ = 'Produto'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    categoria = Column(String)
    preco = Column(Float)
    quantidade = Column(Integer)
    estoqueMinimo = Column(Integer)
    ativo = Column(Boolean, default=True)
    criadoEm = Column(DateTime, default=datetime.utcnow)
    atualizadoEm = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
