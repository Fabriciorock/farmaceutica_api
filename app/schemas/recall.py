import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator


class RecallCreate(BaseModel):
    motivo: str
    descricao: str | None = None
    lote_ids: list[uuid.UUID]

    @field_validator("motivo")
    @classmethod
    def motivo_nao_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Motivo do recall não pode ser vazio.")
        return v.strip()

    @field_validator("lote_ids")
    @classmethod
    def deve_ter_pelo_menos_um_lote(cls, v: list) -> list:
        if len(v) == 0:
            raise ValueError("Recall deve afetar pelo menos um lote.")
        return v


class RecallResponse(BaseModel):
    id: uuid.UUID
    motivo: str
    descricao: str | None
    data_emissao: datetime
    lotes_afetados: list[uuid.UUID] = []
    pedidos_bloqueados: list[uuid.UUID] = []
    model_config = ConfigDict(from_attributes=True)