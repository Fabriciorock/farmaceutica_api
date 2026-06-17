from datetime import date
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.enums import (
    StatusPedidoEnum, StatusLoteEnum,
    TRANSICOES_PEDIDO, ESTADOS_TERMINAIS_PEDIDO
)
from app.repositories.pedido_repository import PedidoRepository
from app.repositories.lote_repository import LoteRepository
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.item_pedido_repository import ItemPedidoRepository
from app.schemas.pedido import PedidoCreate
from app.schemas.item_pedido import ItemPedidoCreate
from app.core.exceptions import (
    NotFoundException, EstadoTerminalException, TransicaoInvalidaException,
    LoteIndisponivelException, LoteVencidoException, SaldoInsuficienteException,
    AutorizacaoInsuficienteException, PedidoSemItensException
)


class PedidoService:

    def __init__(self, db: Session):
        self.repo = PedidoRepository(db)
        self.lote_repo = LoteRepository(db)
        self.cliente_repo = ClienteRepository(db)
        self.item_repo = ItemPedidoRepository(db)

    def criar(self, dados: PedidoCreate) -> Pedido:
        cliente = self.cliente_repo.get_by_id(dados.cliente_id)
        if not cliente:
            raise NotFoundException("Cliente", str(dados.cliente_id))
        pedido = Pedido(cliente_id=dados.cliente_id)
        return self.repo.salvar(pedido)

    def buscar_por_id(self, pedido_id: UUID) -> Pedido:
        pedido = self.repo.get_by_id(pedido_id)
        if not pedido:
            raise NotFoundException("Pedido", str(pedido_id))
        return pedido

    def listar(self, pagina: int = 1, por_pagina: int = 10) -> tuple[list[Pedido], int]:
        skip = (pagina - 1) * por_pagina
        return self.repo.listar(skip, por_pagina), self.repo.contar()

    def adicionar_item(self, pedido_id: UUID, dados: ItemPedidoCreate) -> ItemPedido:
        pedido = self.buscar_por_id(pedido_id)

        # RN-006: pedido em estado terminal não aceita novos itens
        status_atual = StatusPedidoEnum(pedido.status)
        if status_atual in ESTADOS_TERMINAIS_PEDIDO:
            raise EstadoTerminalException("Pedido", pedido.status)

        lote = self.lote_repo.get_by_id(dados.lote_id)
        if not lote:
            raise NotFoundException("Lote", str(dados.lote_id))

        # RN-001 e RN-008: lote deve estar disponível
        if lote.status != StatusLoteEnum.DISPONIVEL.value:
            raise LoteIndisponivelException(lote.codigo_lote, lote.status)

        # RN-002: lote não pode estar vencido
        if lote.data_validade < date.today():
            raise LoteVencidoException(lote.codigo_lote)

        # RN-004: saldo disponível do lote deve ser suficiente
        saldo = self.lote_repo.calcular_saldo(dados.lote_id)
        if dados.quantidade > saldo:
            raise SaldoInsuficienteException(
                lote.codigo_lote, dados.quantidade, saldo
            )

        item = ItemPedido(
            pedido_id=pedido_id,
            lote_id=dados.lote_id,
            quantidade=dados.quantidade,
            preco_unitario_momento=lote.produto.preco_unitario
        )
        self.item_repo.salvar(item)
        self.repo.recalcular_valor_total(pedido_id)
        return item

    def transicionar_status(self, pedido_id: UUID, novo_status: StatusPedidoEnum) -> Pedido:
        pedido = self.buscar_por_id(pedido_id)

        # RN-006: estado terminal não aceita transições
        status_atual = StatusPedidoEnum(pedido.status)
        if status_atual in ESTADOS_TERMINAIS_PEDIDO:
            raise EstadoTerminalException("Pedido", pedido.status)

        # RN-005: valida transição pela máquina de estados
        if novo_status not in TRANSICOES_PEDIDO[status_atual]:
            raise TransicaoInvalidaException(
                "Pedido", pedido.status, novo_status.value
            )

        # RN-003: ao confirmar, verifica autorização para controlados
        if novo_status == StatusPedidoEnum.CONFIRMADO:
            self._verificar_autorizacao_controlados(pedido)
            if not pedido.itens:
                raise PedidoSemItensException()

        pedido.status = novo_status.value
        return self.repo.salvar(pedido)

    def _verificar_autorizacao_controlados(self, pedido: Pedido) -> None:
        """RN-003: verifica se cliente tem autorização vigente para controlados."""
        from app.models.enums import CategoriaEnum
        tem_controlado = any(
            item.lote.produto.categoria == CategoriaEnum.MEDICAMENTO_CONTROLADO
            for item in pedido.itens
        )
        if not tem_controlado:
            return

        cliente = pedido.cliente
        autorizacao_valida = (
            cliente.autorizado_controlados
            and cliente.validade_autorizacao is not None
            and cliente.validade_autorizacao >= date.today()
        )
        if not autorizacao_valida:
            raise AutorizacaoInsuficienteException()