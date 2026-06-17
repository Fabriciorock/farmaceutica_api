from enum import Enum


class CategoriaEnum(str, Enum):
    MEDICAMENTO_CONTROLADO = "medicamento_controlado"
    MEDICAMENTO_COMUM = "medicamento_comum"
    COSMETICO = "cosmetico"


class StatusLoteEnum(str, Enum):
    EM_PRODUCAO = "em_producao"
    EM_ANALISE_QUALIDADE = "em_analise_qualidade"
    APROVADO = "aprovado"
    REPROVADO = "reprovado"
    DISPONIVEL = "disponivel"
    ESGOTADO = "esgotado"
    RECOLHIDO = "recolhido"


class ResultadoQualidadeEnum(str, Enum):
    APROVADO = "aprovado"
    REPROVADO = "reprovado"


class TipoClienteEnum(str, Enum):
    FARMACIA = "farmacia"
    DISTRIBUIDOR = "distribuidor"
    HOSPITAL = "hospital"


class StatusPedidoEnum(str, Enum):
    RASCUNHO = "rascunho"
    CONFIRMADO = "confirmado"
    FATURADO = "faturado"
    ENVIADO = "enviado"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"
    BLOQUEADO_RECALL = "bloqueado_recall"


# ── Máquinas de estado ────────────────────────────────────────────────────────

TRANSICOES_LOTE: dict[StatusLoteEnum, set[StatusLoteEnum]] = {
    StatusLoteEnum.EM_PRODUCAO:          {StatusLoteEnum.EM_ANALISE_QUALIDADE},
    StatusLoteEnum.EM_ANALISE_QUALIDADE: {StatusLoteEnum.APROVADO, StatusLoteEnum.REPROVADO},
    StatusLoteEnum.APROVADO:             {StatusLoteEnum.DISPONIVEL},
    StatusLoteEnum.DISPONIVEL:           {StatusLoteEnum.ESGOTADO, StatusLoteEnum.RECOLHIDO},
    StatusLoteEnum.ESGOTADO:             {StatusLoteEnum.RECOLHIDO},
    StatusLoteEnum.REPROVADO:            set(),  # terminal
    StatusLoteEnum.RECOLHIDO:            set(),  # terminal
}

TRANSICOES_PEDIDO: dict[StatusPedidoEnum, set[StatusPedidoEnum]] = {
    StatusPedidoEnum.RASCUNHO:         {StatusPedidoEnum.CONFIRMADO, StatusPedidoEnum.CANCELADO},
    StatusPedidoEnum.CONFIRMADO:       {StatusPedidoEnum.FATURADO, StatusPedidoEnum.CANCELADO, StatusPedidoEnum.BLOQUEADO_RECALL},
    StatusPedidoEnum.FATURADO:         {StatusPedidoEnum.ENVIADO, StatusPedidoEnum.BLOQUEADO_RECALL},
    StatusPedidoEnum.ENVIADO:          {StatusPedidoEnum.ENTREGUE, StatusPedidoEnum.BLOQUEADO_RECALL},
    StatusPedidoEnum.ENTREGUE:         set(),  # terminal
    StatusPedidoEnum.CANCELADO:        set(),  # terminal
    StatusPedidoEnum.BLOQUEADO_RECALL: {StatusPedidoEnum.CANCELADO},
}

ESTADOS_TERMINAIS_PEDIDO = {StatusPedidoEnum.ENTREGUE, StatusPedidoEnum.CANCELADO}