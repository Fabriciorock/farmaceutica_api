from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.lote import Lote
from app.models.item_pedido import ItemPedido
from app.models.pedido import Pedido
from app.models.enums import StatusLoteEnum, StatusPedidoEnum
from app.repositories.base import BaseRepository


class LoteRepository(BaseRepository[Lote]):

    def __init__(self, db: Session):
        super().__init__(Lote, db)

    def get_by_codigo(self, codigo_lote: str) -> Lote | None:
        return self.db.query(Lote).filter(Lote.codigo_lote == codigo_lote).first()

    def calcular_saldo(self, lote_id: UUID) -> int:
        """
        Saldo disponível = quantidade_produzida − Σ quantidades vendidas
        em pedidos não cancelados.
        """
        lote = self.get_by_id(lote_id)
        if not lote:
            return 0

        vendido = (
            self.db.query(func.coalesce(func.sum(ItemPedido.quantidade), 0))
            .join(Pedido, Pedido.id == ItemPedido.pedido_id)
            .filter(
                ItemPedido.lote_id == lote_id,
                Pedido.status.notin_([StatusPedidoEnum.CANCELADO])
            )
            .scalar()
        )
        return lote.quantidade_produzida - int(vendido)

    def listar_por_status(self, status: StatusLoteEnum) -> list[Lote]:
        return self.db.query(Lote).filter(Lote.status == status).all()