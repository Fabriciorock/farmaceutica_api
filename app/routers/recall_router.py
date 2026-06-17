from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.recall import RecallCreate, RecallResponse
from app.schemas.base import RespostaPaginada
from app.services.recall_service import RecallService
import math

router = APIRouter(prefix="/recalls", tags=["Recalls"])


@router.post("/", status_code=201)
def emitir_recall(dados: RecallCreate, db: Session = Depends(get_db)):
    recall, pedidos_bloqueados = RecallService(db).emitir(dados)
    return {
        "id": recall.id,
        "motivo": recall.motivo,
        "descricao": recall.descricao,
        "data_emissao": recall.data_emissao,
        "lotes_afetados": [lote.id for lote in recall.lotes],
        "pedidos_bloqueados": pedidos_bloqueados
    }


@router.get("/", response_model=RespostaPaginada[RecallResponse])
def listar_recalls(pagina: int = 1, por_pagina: int = 10, db: Session = Depends(get_db)):
    itens, total = RecallService(db).listar(pagina, por_pagina)
    return RespostaPaginada(
        itens=itens, total=total, pagina=pagina,
        por_pagina=por_pagina, paginas=math.ceil(total / por_pagina)
    )