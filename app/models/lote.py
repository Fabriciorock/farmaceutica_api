import uuid
from datetime import date

from sqlalchemy import String, Integer, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import StatusLoteEnum


class Lote(Base):
    __tablename__ = "lotes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    produto_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("produtos.id"), nullable=False)
    codigo_lote: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    data_fabricacao: Mapped[date] = mapped_column(Date, nullable=False)
    data_validade: Mapped[date] = mapped_column(Date, nullable=False)
    quantidade_produzida: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default=StatusLoteEnum.EM_PRODUCAO.value)

    produto: Mapped["Produto"] = relationship("Produto", back_populates="lotes")
    controles_qualidade: Mapped[list["ControleQualidade"]] = relationship("ControleQualidade", back_populates="lote", cascade="all, delete-orphan")
    itens_pedido: Mapped[list["ItemPedido"]] = relationship("ItemPedido", back_populates="lote")
    recalls: Mapped[list["Recall"]] = relationship("Recall", secondary="recall_lote", back_populates="lotes")