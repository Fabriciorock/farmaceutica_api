import uuid
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, field_validator
from app.models.enums import CategoriaEnum


class ProdutoBase(BaseModel):
    nome: str
    categoria: CategoriaEnum
    fabricante: str
    principio_ativo: str | None = None
    preco_unitario: Decimal
    requer_autorizacao: bool = False

    @field_validator("preco_unitario")
    @classmethod
    def preco_deve_ser_positivo(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("Preço unitário deve ser maior que zero.")
        return v

    @field_validator("nome", "fabricante")
    @classmethod
    def nao_pode_ser_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Campo não pode ser vazio.")
        return v.strip()


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(BaseModel):
    nome: str | None = None
    fabricante: str | None = None
    principio_ativo: str | None = None
    preco_unitario: Decimal | None = None
    requer_autorizacao: bool | None = None


class ProdutoResponse(ProdutoBase):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)