from uuid import UUID
from sqlalchemy.orm import Session
from app.models.controle_qualidade import ControleQualidade
from app.repositories.base import BaseRepository


class ControleQualidadeRepository(BaseRepository[ControleQualidade]):

    def __init__(self, db: Session):
        super().__init__(ControleQualidade, db)

    def listar_por_lote(self, lote_id: UUID) -> list[ControleQualidade]:
        return (
            self.db.query(ControleQualidade)
            .filter(ControleQualidade.lote_id == lote_id)
            .order_by(ControleQualidade.data_analise.desc())
            .all()
        )