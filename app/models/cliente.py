import uuid
from datetime import date

from sqlalchemy import String, Boolean, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    razao_social: Mapped[str] = mapped_column(String(300), nullable=False)
    cnpj: Mapped[str] = mapped_column(String(18), nullable=False, unique=True)
    tipo: Mapped[str] = mapped_column(String(30), nullable=False)
    autorizado_controlados: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    validade_autorizacao: Mapped[date | None] = mapped_column(Date, nullable=True)

    pedidos: Mapped[list["Pedido"]] = relationship("Pedido", back_populates="cliente")