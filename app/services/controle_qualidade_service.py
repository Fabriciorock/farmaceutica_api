from uuid import UUID
from sqlalchemy.orm import Session
from app.models.controle_qualidade import ControleQualidade
from app.models.enums import ResultadoQualidadeEnum, StatusLoteEnum, TRANSICOES_LOTE
from app.repositories.controle_qualidade_repository import ControleQualidadeRepository
from app.repositories.lote_repository import LoteRepository
from app.schemas.controle_qualidade import ControleQualidadeCreate
from app.core.exceptions import NotFoundException, TransicaoInvalidaException


class ControleQualidadeService:

    def __init__(self, db: Session):
        self.repo = ControleQualidadeRepository(db)
        self.lote_repo = LoteRepository(db)

    def registrar(self, dados: ControleQualidadeCreate) -> ControleQualidade:
        """
        Registra análise e atualiza status do lote automaticamente.
        APROVADO → lote vai para 'aprovado'
        REPROVADO → lote vai para 'reprovado'
        """
        lote = self.lote_repo.get_by_id(dados.lote_id)
        if not lote:
            raise NotFoundException("Lote", str(dados.lote_id))

        # Determina novo status do lote com base no resultado
        if dados.resultado == ResultadoQualidadeEnum.APROVADO:
            novo_status = StatusLoteEnum.APROVADO
        else:
            novo_status = StatusLoteEnum.REPROVADO

        # Valida transição pela máquina de estados
        if novo_status not in TRANSICOES_LOTE[lote.status]:
            raise TransicaoInvalidaException(
                "Lote", lote.status.value, novo_status.value
            )

        # Salva o controle de qualidade
        controle = ControleQualidade(**dados.model_dump())
        self.repo.salvar(controle)

        # Atualiza status do lote
        lote.status = novo_status
        self.lote_repo.salvar(lote)

        return controle

    def listar_por_lote(self, lote_id: UUID) -> list[ControleQualidade]:
        return self.repo.listar_por_lote(lote_id)