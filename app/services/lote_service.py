from uuid import UUID
from sqlalchemy.orm import Session
from app.models.lote import Lote
from app.models.enums import StatusLoteEnum, TRANSICOES_LOTE
from app.repositories.lote_repository import LoteRepository
from app.schemas.lote import LoteCreate, LoteUpdate
from app.core.exceptions import (
    NotFoundException, TransicaoInvalidaException
)


class LoteService:

    def __init__(self, db: Session):
        self.repo = LoteRepository(db)

    def criar(self, dados: LoteCreate) -> Lote:
        lote = Lote(**dados.model_dump())
        return self.repo.salvar(lote)

    def buscar_por_id(self, lote_id: UUID) -> Lote:
        lote = self.repo.get_by_id(lote_id)
        if not lote:
            raise NotFoundException("Lote", str(lote_id))
        return lote

    def listar(self, pagina: int = 1, por_pagina: int = 10) -> tuple[list[Lote], int]:
        skip = (pagina - 1) * por_pagina
        return self.repo.listar(skip, por_pagina), self.repo.contar()

    def atualizar(self, lote_id: UUID, dados: LoteUpdate) -> Lote:
        lote = self.buscar_por_id(lote_id)
        for campo, valor in dados.model_dump(exclude_none=True).items():
            setattr(lote, campo, valor)
        return self.repo.salvar(lote)

    def transicionar_status(self, lote_id: UUID, novo_status: StatusLoteEnum) -> Lote:
        """RN-005: Valida e executa transição de estado do lote."""
        lote = self.buscar_por_id(lote_id)
        status_atual = StatusLoteEnum(lote.status)  # converte string → enum
        transicoes_permitidas = TRANSICOES_LOTE[status_atual]

        if novo_status not in transicoes_permitidas:
            raise TransicaoInvalidaException(
                "Lote", lote.status, novo_status.value
            )

        lote.status = novo_status.value
        return self.repo.salvar(lote)

    def calcular_saldo(self, lote_id: UUID) -> int:
        return self.repo.calcular_saldo(lote_id)