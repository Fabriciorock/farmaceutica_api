from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


# ── Exceções de domínio ───────────────────────────────────────────────────────

class DomainException(Exception):
    """Base para todas as exceções de regra de negócio."""
    def __init__(self, message: str, status_code: int = 422):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class LoteIndisponivelException(DomainException):
    """RN-001: Lote não está com status disponivel."""
    def __init__(self, codigo_lote: str, status_atual: str):
        super().__init__(
            f"Lote '{codigo_lote}' não está disponível (status atual: {status_atual}).",
            status_code=422
        )


class LoteVencidoException(DomainException):
    """RN-002: Data de validade do lote já passou."""
    def __init__(self, codigo_lote: str):
        super().__init__(
            f"Lote '{codigo_lote}' está com validade expirada.",
            status_code=422
        )


class AutorizacaoInsuficienteException(DomainException):
    """RN-003: Cliente sem autorização vigente para medicamentos controlados."""
    def __init__(self):
        super().__init__(
            "Cliente não possui autorização vigente para medicamentos controlados.",
            status_code=403
        )


class SaldoInsuficienteException(DomainException):
    """RN-004: Quantidade solicitada excede o saldo disponível do lote."""
    def __init__(self, codigo_lote: str, solicitado: int, disponivel: int):
        super().__init__(
            f"Saldo insuficiente no lote '{codigo_lote}': "
            f"solicitado={solicitado}, disponível={disponivel}.",
            status_code=422
        )


class TransicaoInvalidaException(DomainException):
    """RN-005: Transição de estado não permitida pela máquina de estados."""
    def __init__(self, entidade: str, de: str, para: str):
        super().__init__(
            f"Transição inválida para {entidade}: '{de}' → '{para}' não é permitida.",
            status_code=422
        )


class EstadoTerminalException(DomainException):
    """RN-006: Entidade em estado terminal não pode ser modificada."""
    def __init__(self, entidade: str, status: str):
        super().__init__(
            f"{entidade} em estado terminal ('{status}') não pode ser modificado.",
            status_code=409
        )


class PedidoSemItensException(DomainException):
    """Pedido vazio não pode ser confirmado."""
    def __init__(self):
        super().__init__(
            "Pedido não pode ser confirmado sem itens.",
            status_code=422
        )


class EntidadeEmUsoException(DomainException):
    """Entidade pai não pode ser deletada pois possui dependentes ativos."""
    def __init__(self, entidade: str, dependente: str):
        super().__init__(
            f"{entidade} não pode ser removido pois possui {dependente} ativo(s).",
            status_code=409
        )


class NotFoundException(DomainException):
    """Recurso não encontrado."""
    def __init__(self, entidade: str, id: str):
        super().__init__(
            f"{entidade} com id '{id}' não encontrado.",
            status_code=404
        )


# ── Handler global ────────────────────────────────────────────────────────────

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.message,
                "tipo": type(exc).__name__
            }
        )