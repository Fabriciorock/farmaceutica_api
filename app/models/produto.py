import uuid
from decimal import Decimal

from sqlalchemy import String, Boolean, Numeric, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import CategoriaEnum


class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    categoria: Mapped[str] = mapped_column(String(50), nullable=False)
    fabricante: Mapped[str] = mapped_column(String(200), nullable=False)
    principio_ativo: Mapped[str | None] = mapped_column(String(300), nullable=True)
    preco_unitario: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    requer_autorizacao: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    lotes: Mapped[list["Lote"]] = relationship("Lote", back_populates="produto", cascade="all, delete-orphan")