from uuid import UUID
from sqlalchemy.orm import Session
from app.models.item_pedido import ItemPedido
from app.repositories.base import BaseRepository


class ItemPedidoRepository(BaseRepository[ItemPedido]):

    def __init__(self, db: Session):
        super().__init__(ItemPedido, db)

    def listar_por_pedido(self, pedido_id: UUID) -> list[ItemPedido]:
        return (
            self.db.query(ItemPedido)
            .filter(ItemPedido.pedido_id == pedido_id)
            .all()
        )