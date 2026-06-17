from sqlalchemy.orm import Session
from app.models.recall import Recall
from app.models.enums import StatusLoteEnum, StatusPedidoEnum
from app.repositories.recall_repository import RecallRepository
from app.repositories.lote_repository import LoteRepository
from app.repositories.pedido_repository import PedidoRepository
from app.schemas.recall import RecallCreate
from app.core.exceptions import NotFoundException
import uuid


class RecallService:

    def __init__(self, db: Session):
        self.repo = RecallRepository(db)
        self.lote_repo = LoteRepository(db)
        self.pedido_repo = PedidoRepository(db)

    def emitir(self, dados: RecallCreate) -> tuple[Recall, list[uuid.UUID]]:
        """
        RN-007 e RN-008: Emite recall, recolhe lotes e bloqueia
        automaticamente todos os pedidos ativos que contêm esses lotes.
        Tudo ocorre dentro da mesma transação.
        """
        # Valida e coleta os lotes afetados
        lotes = []
        for lote_id in dados.lote_ids:
            lote = self.lote_repo.get_by_id(lote_id)
            if not lote:
                raise NotFoundException("Lote", str(lote_id))
            lotes.append(lote)

        # Cria o recall
        recall = Recall(
            motivo=dados.motivo,
            descricao=dados.descricao,
            lotes=lotes
        )
        self.repo.salvar(recall)

        # Recolhe os lotes e bloqueia pedidos ativos
        pedidos_bloqueados = []
        for lote in lotes:
            # Atualiza status do lote para recolhido
            estados_validos = {StatusLoteEnum.DISPONIVEL, StatusLoteEnum.ESGOTADO}
            if lote.status in estados_validos:
                lote.status = StatusLoteEnum.RECOLHIDO
                self.lote_repo.salvar(lote)

            # Bloqueia pedidos ativos que contêm esse lote
            pedidos_ativos = self.pedido_repo.listar_ativos_com_lote(lote.id)
            for pedido in pedidos_ativos:
                pedido.status = StatusPedidoEnum.BLOQUEADO_RECALL
                self.pedido_repo.salvar(pedido)
                pedidos_bloqueados.append(pedido.id)

        return recall, pedidos_bloqueados

    def listar(self, pagina: int = 1, por_pagina: int = 10) -> tuple[list[Recall], int]:
        skip = (pagina - 1) * por_pagina
        return self.repo.listar(skip, por_pagina), self.repo.contar()