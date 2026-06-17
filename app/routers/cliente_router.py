from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from app.schemas.base import RespostaPaginada
from app.services.cliente_service import ClienteService
import math

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/", response_model=ClienteResponse, status_code=201)
def criar_cliente(dados: ClienteCreate, db: Session = Depends(get_db)):
    return ClienteService(db).criar(dados)


@router.get("/", response_model=RespostaPaginada[ClienteResponse])
def listar_clientes(pagina: int = 1, por_pagina: int = 10, db: Session = Depends(get_db)):
    itens, total = ClienteService(db).listar(pagina, por_pagina)
    return RespostaPaginada(
        itens=itens, total=total, pagina=pagina,
        por_pagina=por_pagina, paginas=math.ceil(total / por_pagina)
    )


@router.get("/{cliente_id}", response_model=ClienteResponse)
def buscar_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    return ClienteService(db).buscar_por_id(cliente_id)


@router.patch("/{cliente_id}", response_model=ClienteResponse)
def atualizar_cliente(cliente_id: UUID, dados: ClienteUpdate, db: Session = Depends(get_db)):
    return ClienteService(db).atualizar(cliente_id, dados)