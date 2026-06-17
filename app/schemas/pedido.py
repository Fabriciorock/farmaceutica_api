import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from app.models.enums import StatusPedidoEnum


class PedidoCreate(BaseModel):
    cliente_id: uuid.UUID


class PedidoStatusUpdate(BaseModel):
    """Schema exclusivo para transição de status via maquina de estados."""
    novo_status: StatusPedidoEnum


class PedidoResponse(BaseModel):
    id: uuid.UUID
    cliente_id: uuid.UUID
    data_pedido: datetime
    status: StatusPedidoEnum
    valor_total: Decimal
    model_config = ConfigDict(from_attributes=True)