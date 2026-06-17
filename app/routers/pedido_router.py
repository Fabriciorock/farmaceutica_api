from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.pedido import PedidoCreate, PedidoStatusUpdate, PedidoResponse
from app.schemas.item_pedido import ItemPedidoCreate, ItemPedidoResponse
from app.schemas.base import RespostaPaginada
from app.services.pedido_service import PedidoService
import math

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("/", response_model=PedidoResponse, status_code=201)
def criar_pedido(dados: PedidoCreate, db: Session = Depends(get_db)):
    return PedidoService(db).criar(dados)


@router.get("/", response_model=RespostaPaginada[PedidoResponse])
def listar_pedidos(pagina: int = 1, por_pagina: int = 10, db: Session = Depends(get_db)):
    itens, total = PedidoService(db).listar(pagina, por_pagina)
    return RespostaPaginada(
        itens=itens, total=total, pagina=pagina,
        por_pagina=por_pagina, paginas=math.ceil(total / por_pagina)
    )


@router.get("/{pedido_id}", response_model=PedidoResponse)
def buscar_pedido(pedido_id: UUID, db: Session = Depends(get_db)):
    return PedidoService(db).buscar_por_id(pedido_id)


@router.post("/{pedido_id}/itens", response_model=ItemPedidoResponse, status_code=201)
def adicionar_item(pedido_id: UUID, dados: ItemPedidoCreate, db: Session = Depends(get_db)):
    return PedidoService(db).adicionar_item(pedido_id, dados)


@router.patch("/{pedido_id}/status", response_model=PedidoResponse)
def transicionar_status(pedido_id: UUID, dados: PedidoStatusUpdate, db: Session = Depends(get_db)):
    return PedidoService(db).transicionar_status(pedido_id, dados.novo_status)