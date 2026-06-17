import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ControleQualidade(Base):
    __tablename__ = "controles_qualidade"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lote_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("lotes.id"), nullable=False)
    data_analise: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    responsavel: Mapped[str] = mapped_column(String(200), nullable=False)
    resultado: Mapped[str] = mapped_column(String(20), nullable=False)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)

    lote: Mapped["Lote"] = relationship("Lote", back_populates="controles_qualidade")