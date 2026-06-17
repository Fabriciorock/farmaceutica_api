from uuid import UUID
from sqlalchemy.orm import Session
from app.models.produto import Produto
from app.repositories.produto_repository import ProdutoRepository
from app.schemas.produto import ProdutoCreate, ProdutoUpdate
from app.core.exceptions import NotFoundException, EntidadeEmUsoException


class ProdutoService:

    def __init__(self, db: Session):
        self.repo = ProdutoRepository(db)

    def criar(self, dados: ProdutoCreate) -> Produto:
        produto = Produto(**dados.model_dump())
        return self.repo.salvar(produto)

    def buscar_por_id(self, produto_id: UUID) -> Produto:
        produto = self.repo.get_by_id(produto_id)
        if not produto:
            raise NotFoundException("Produto", str(produto_id))
        return produto

    def listar(self, pagina: int = 1, por_pagina: int = 10) -> tuple[list[Produto], int]:
        skip = (pagina - 1) * por_pagina
        return self.repo.listar(skip, por_pagina), self.repo.contar()

    def atualizar(self, produto_id: UUID, dados: ProdutoUpdate) -> Produto:
        produto = self.buscar_por_id(produto_id)
        for campo, valor in dados.model_dump(exclude_none=True).items():
            setattr(produto, campo, valor)
        return self.repo.salvar(produto)

    def deletar(self, produto_id: UUID) -> None:
        produto = self.buscar_por_id(produto_id)
        # Cenário de borda: produto com lotes ativos não pode ser deletado
        if self.repo.tem_lotes_ativos(produto_id):
            raise EntidadeEmUsoException("Produto", "lotes ativos")
        self.repo.deletar(produto)