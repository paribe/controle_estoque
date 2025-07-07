from models import Produto
from database import SessionLocal

def listar_produtos():
    db = SessionLocal()
    produtos = db.query(Produto).filter(Produto.ativo == True).all()
    db.close()
    return produtos

def cadastrar_produto(data):
    db = SessionLocal()
    novo = Produto(**data)
    db.add(novo)
    db.commit()
    db.close()

def atualizar_produto(id, data):
    db = SessionLocal()
    produto = db.query(Produto).filter(Produto.id == id).first()
    for key, value in data.items():
        setattr(produto, key, value)
    db.commit()
    db.close()

def remover_produto(id):
    db = SessionLocal()
    produto = db.query(Produto).filter(Produto.id == id).first()
    produto.ativo = False
    db.commit()
    db.close()

def buscar_produto_por_id(id):
    db = SessionLocal()
    produto = db.query(Produto).filter(Produto.id == id, Produto.ativo == True).first()
    db.close()
    return produto

def baixar_estoque(id, quantidade):
    db = SessionLocal()
    produto = db.query(Produto).filter(Produto.id == id, Produto.ativo == True).first()
    if produto and produto.quantidade >= quantidade:
        produto.quantidade -= quantidade
        db.commit()
        db.close()
        return True
    db.close()
    return False
