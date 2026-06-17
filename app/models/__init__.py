from app.core.database import Base
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

# Tabela intermediária do relacionamento N:N entre Recall e Lote
recall_lote = Table(
    "recall_lote",
    Base.metadata,
    Column("recall_id", UUID(as_uuid=True), ForeignKey("recalls.id", ondelete="CASCADE"), primary_key=True),
    Column("lote_id",   UUID(as_uuid=True), ForeignKey("lotes.id",   ondelete="CASCADE"), primary_key=True),
)

# Importa todos os models para o SQLAlchemy e Alembic os reconhecerem
from app.models.produto import Produto
from app.models.cliente import Cliente
from app.models.lote import Lote
from app.models.controle_qualidade import ControleQualidade
from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.recall import Recall