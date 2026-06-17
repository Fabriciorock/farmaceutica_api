from sqlalchemy.orm import Session
from app.models.produto import Produto
from app.models.enums import StatusLoteEnum
from app.repositories.base import BaseRepository


class ProdutoRepository(BaseRepository[Produto]):

    def __init__(self, db: Session):
        super().__init__(Produto, db)

    def tem_lotes_ativos(self, produto_id) -> bool:
        """Verifica se o produto tem lotes em estados não terminais."""
        estados_terminais = [StatusLoteEnum.REPROVADO, StatusLoteEnum.RECOLHIDO]
        from app.models.lote import Lote
        return (
            self.db.query(Lote)
            .filter(
                Lote.produto_id == produto_id,
                Lote.status.notin_(estados_terminais)
            )
            .first() is not None
        )