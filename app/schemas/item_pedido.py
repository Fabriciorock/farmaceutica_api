import uuid
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, field_validator


class ItemPedidoCreate(BaseModel):
    lote_id: uuid.UUID
    quantidade: int

    @field_validator("quantidade")
    @classmethod
    def quantidade_deve_ser_positiva(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Quantidade deve ser maior que zero.")
        return v


class ItemPedidoResponse(BaseModel):
    id: uuid.UUID
    pedido_id: uuid.UUID
    lote_id: uuid.UUID
    quantidade: int
    preco_unitario_momento: Decimal
    model_config = ConfigDict(from_attributes=True)