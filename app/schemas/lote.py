import uuid
from datetime import date
from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from app.models.enums import StatusLoteEnum


class LoteBase(BaseModel):
    produto_id: uuid.UUID
    codigo_lote: str
    data_fabricacao: date
    data_validade: date
    quantidade_produzida: int

    @field_validator("quantidade_produzida")
    @classmethod
    def quantidade_deve_ser_positiva(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Quantidade produzida deve ser maior que zero.")
        return v

    @field_validator("codigo_lote")
    @classmethod
    def codigo_nao_pode_ser_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Código do lote não pode ser vazio.")
        return v.strip().upper()

    @model_validator(mode="after")
    def validade_deve_ser_apos_fabricacao(self) -> "LoteBase":
        if self.data_validade <= self.data_fabricacao:
            raise ValueError(
                "Data de validade deve ser posterior a data de fabricação."
            )
        return self


class LoteCreate(LoteBase):
    pass


class LoteUpdate(BaseModel):
    data_validade: date | None = None
    quantidade_produzida: int | None = None


class LoteStatusUpdate(BaseModel):
    """Schema exclusivo para transição de status via maquina de estados."""
    novo_status: StatusLoteEnum


class LoteResponse(LoteBase):
    id: uuid.UUID
    status: StatusLoteEnum
    model_config = ConfigDict(from_attributes=True)