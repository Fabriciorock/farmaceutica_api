from uuid import UUID
from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.repositories.cliente_repository import ClienteRepository
from app.schemas.cliente import ClienteCreate, ClienteUpdate
from app.core.exceptions import NotFoundException


class ClienteService:

    def __init__(self, db: Session):
        self.repo = ClienteRepository(db)

    def criar(self, dados: ClienteCreate) -> Cliente:
        cliente = Cliente(**dados.model_dump())
        return self.repo.salvar(cliente)

    def buscar_por_id(self, cliente_id: UUID) -> Cliente:
        cliente = self.repo.get_by_id(cliente_id)
        if not cliente:
            raise NotFoundException("Cliente", str(cliente_id))
        return cliente

    def listar(self, pagina: int = 1, por_pagina: int = 10) -> tuple[list[Cliente], int]:
        skip = (pagina - 1) * por_pagina
        return self.repo.listar(skip, por_pagina), self.repo.contar()

    def atualizar(self, cliente_id: UUID, dados: ClienteUpdate) -> Cliente:
        cliente = self.buscar_por_id(cliente_id)
        for campo, valor in dados.model_dump(exclude_none=True).items():
            setattr(cliente, campo, valor)
        return self.repo.salvar(cliente)