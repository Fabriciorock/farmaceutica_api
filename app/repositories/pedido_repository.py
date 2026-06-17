from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.enums import StatusPedidoEnum
from app.repositories.base import BaseRepository


class PedidoRepository(BaseRepository[Pedido]):

    def __init__(self, db: Session):
        super().__init__(Pedido, db)

    def listar_por_cliente(self, cliente_id: UUID) -> list[Pedido]:
        return (
            self.db.query(Pedido)
            .filter(Pedido.cliente_id == cliente_id)
            .all()
        )

    def listar_ativos_com_lote(self, lote_id: UUID) -> list[Pedido]:
        """
        Retorna pedidos em estados ativos que contêm um lote específico.
        Usado pelo recall para bloquear pedidos automaticamente.
        """
        estados_ativos = [
            StatusPedidoEnum.CONFIRMADO,
            StatusPedidoEnum.FATURADO,
            StatusPedidoEnum.ENVIADO,
        ]
        return (
            self.db.query(Pedido)
            .join(ItemPedido, ItemPedido.pedido_id == Pedido.id)
            .filter(
                ItemPedido.lote_id == lote_id,
                Pedido.status.in_(estados_ativos)
            )
            .all()
        )

    def recalcular_valor_total(self, pedido_id: UUID) -> None:
        """Atualiza o cache valor_total somando os itens do pedido."""
        total = (
            self.db.query(
                func.coalesce(
                    func.sum(ItemPedido.quantidade * ItemPedido.preco_unitario_momento),
                    0
                )
            )
            .filter(ItemPedido.pedido_id == pedido_id)
            .scalar()
        )
        self.db.query(Pedido).filter(Pedido.id == pedido_id).update(
            {"valor_total": total}
        )
        self.db.commit()