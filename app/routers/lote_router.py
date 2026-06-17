from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.lote import LoteCreate, LoteUpdate, LoteStatusUpdate, LoteResponse
from app.schemas.base import RespostaPaginada
from app.services.lote_service import LoteService
import math

router = APIRouter(prefix="/lotes", tags=["Lotes"])


@router.post("/", response_model=LoteResponse, status_code=201)
def criar_lote(dados: LoteCreate, db: Session = Depends(get_db)):
    return LoteService(db).criar(dados)


@router.get("/", response_model=RespostaPaginada[LoteResponse])
def listar_lotes(pagina: int = 1, por_pagina: int = 10, db: Session = Depends(get_db)):
    itens, total = LoteService(db).listar(pagina, por_pagina)
    return RespostaPaginada(
        itens=itens, total=total, pagina=pagina,
        por_pagina=por_pagina, paginas=math.ceil(total / por_pagina)
    )


@router.get("/{lote_id}", response_model=LoteResponse)
def buscar_lote(lote_id: UUID, db: Session = Depends(get_db)):
    return LoteService(db).buscar_por_id(lote_id)


@router.get("/{lote_id}/saldo")
def saldo_lote(lote_id: UUID, db: Session = Depends(get_db)):
    saldo = LoteService(db).calcular_saldo(lote_id)
    return {"lote_id": lote_id, "saldo_disponivel": saldo}


@router.patch("/{lote_id}", response_model=LoteResponse)
def atualizar_lote(lote_id: UUID, dados: LoteUpdate, db: Session = Depends(get_db)):
    return LoteService(db).atualizar(lote_id, dados)


@router.patch("/{lote_id}/status", response_model=LoteResponse)
def transicionar_status_lote(lote_id: UUID, dados: LoteStatusUpdate, db: Session = Depends(get_db)):
    return LoteService(db).transicionar_status(lote_id, dados.novo_status)