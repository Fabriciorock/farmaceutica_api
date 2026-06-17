import uuid
from decimal import Decimal

from sqlalchemy import Integer, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    pedido_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("pedidos.id"), nullable=False
    )
    lote_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("lotes.id"), nullable=False
    )
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    preco_unitario_momento: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )

    # Relacionamentos
    pedido: Mapped["Pedido"] = relationship("Pedido", back_populates="itens")
    lote: Mapped["Lote"] = relationship("Lote", back_populates="itens_pedido")