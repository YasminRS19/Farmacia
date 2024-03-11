from typing import List

from sqlalchemy import Column, Integer, String, Float

from ext.database import db

associacao_produto = db.Table(
    "produtos_indicacoes",
    db.Model.metadata,
    Column("produto_id", db.ForeignKey("produto.id_produto")),
    Column("indicacao_id", db.ForeignKey("indicacao.id_indicacao")),
)


class Indicacao(db.Model):
    id_indicacao = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)


class Produto(db.Model):
    id_produto = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    preco_compra = Column(Float, nullable=False)
    preco_venda = Column(Float, nullable=False)
    imagem = Column(String, nullable=False)
    substancias = Column(String, nullable=False)

    # Provedor
    provedor_id = db.Column(db.Integer, db.ForeignKey('provedor.id_provedor'))
    indicacoes: db.Mapped[List[Indicacao]] = db.relationship(secondary=associacao_produto)


class Provedor(db.Model):
    id_provedor = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    rfc = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    endereco = Column(String, nullable=False)

    # Produtos
    produtos = db.relationship('Produto', backref='provedor')
