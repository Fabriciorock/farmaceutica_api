from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoResponse
from app.schemas.base import RespostaPaginada
from app.services.produto_service import ProdutoService
import math

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.post("/", response_model=ProdutoResponse, status_code=201)
def criar_produto(dados: ProdutoCreate, db: Session = Depends(get_db)):
    return ProdutoService(db).criar(dados)


@router.get("/", response_model=RespostaPaginada[ProdutoResponse])
def listar_produtos(pagina: int = 1, por_pagina: int = 10, db: Session = Depends(get_db)):
    itens, total = ProdutoService(db).listar(pagina, por_pagina)
    return RespostaPaginada(
        itens=itens, total=total, pagina=pagina,
        por_pagina=por_pagina, paginas=math.ceil(total / por_pagina)
    )


@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(produto_id: UUID, db: Session = Depends(get_db)):
    return ProdutoService(db).buscar_por_id(produto_id)


@router.patch("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(produto_id: UUID, dados: ProdutoUpdate, db: Session = Depends(get_db)):
    return ProdutoService(db).atualizar(produto_id, dados)


@router.delete("/{produto_id}", status_code=204)
def deletar_produto(produto_id: UUID, db: Session = Depends(get_db)):
    ProdutoService(db).deletar(produto_id)