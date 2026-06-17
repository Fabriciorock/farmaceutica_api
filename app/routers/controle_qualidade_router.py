from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.controle_qualidade import ControleQualidadeCreate, ControleQualidadeResponse
from app.services.controle_qualidade_service import ControleQualidadeService

router = APIRouter(prefix="/controle-qualidade", tags=["Controle de Qualidade"])


@router.post("/", response_model=ControleQualidadeResponse, status_code=201)
def registrar_analise(dados: ControleQualidadeCreate, db: Session = Depends(get_db)):
    return ControleQualidadeService(db).registrar(dados)


@router.get("/lote/{lote_id}", response_model=list[ControleQualidadeResponse])
def listar_por_lote(lote_id: UUID, db: Session = Depends(get_db)):
    return ControleQualidadeService(db).listar_por_lote(lote_id)