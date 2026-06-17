import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
from app.models.enums import ResultadoQualidadeEnum


class ControleQualidadeBase(BaseModel):
    lote_id: uuid.UUID
    responsavel: str
    resultado: ResultadoQualidadeEnum
    observacoes: str | None = None

    @field_validator("responsavel")
    @classmethod
    def responsavel_nao_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Nome do responsavel não pode ser vazio.")
        return v.strip()


class ControleQualidadeCreate(ControleQualidadeBase):
    pass


class ControleQualidadeResponse(ControleQualidadeBase):
    id: uuid.UUID
    data_analise: datetime
    model_config = ConfigDict(from_attributes=True)