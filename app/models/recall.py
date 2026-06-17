import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Recall(Base):
    __tablename__ = "recalls"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    motivo: Mapped[str] = mapped_column(String(500), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_emissao: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    # Relacionamento N:N com Lote via tabela intermediária
    lotes: Mapped[list["Lote"]] = relationship(
        "Lote", secondary="recall_lote", back_populates="recalls"
    )