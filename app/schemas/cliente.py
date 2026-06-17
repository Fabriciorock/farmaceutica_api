import uuid
from datetime import date
from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from app.models.enums import TipoClienteEnum


class ClienteBase(BaseModel):
    razao_social: str
    cnpj: str
    tipo: TipoClienteEnum
    autorizado_controlados: bool = False
    validade_autorizacao: date | None = None

    @field_validator("cnpj")
    @classmethod
    def cnpj_valido(cls, v: str) -> str:
        digits = v.replace(".", "").replace("/", "").replace("-", "")
        if len(digits) != 14 or not digits.isdigit():
            raise ValueError("CNPJ deve conter 14 dígitos numéricos.")
        return v.strip()

    @field_validator("razao_social")
    @classmethod
    def razao_social_nao_vazia(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Razão social não pode ser vazia.")
        return v.strip()

    @model_validator(mode="after")
    def autorizacao_exige_validade(self) -> "ClienteBase":
        if self.autorizado_controlados and self.validade_autorizacao is None:
            raise ValueError(
                "Clientes autorizados para medicamentos controlados "
                "devem ter validade_autorizacao informada."
            )
        return self


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    razao_social: str | None = None
    autorizado_controlados: bool | None = None
    validade_autorizacao: date | None = None


class ClienteResponse(ClienteBase):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)