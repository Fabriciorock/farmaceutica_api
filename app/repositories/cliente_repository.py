from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.repositories.base import BaseRepository


class ClienteRepository(BaseRepository[Cliente]):

    def __init__(self, db: Session):
        super().__init__(Cliente, db)

    def get_by_cnpj(self, cnpj: str) -> Cliente | None:
        return self.db.query(Cliente).filter(Cliente.cnpj == cnpj).first()