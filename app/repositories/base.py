from typing import Generic, TypeVar
from uuid import UUID
from sqlalchemy.orm import Session
from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """CRUD genérico reutilizado por todos os repositories."""

    def __init__(self, model: type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: UUID) -> ModelType | None:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def listar(self, skip: int = 0, limit: int = 10) -> list[ModelType]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def contar(self) -> int:
        return self.db.query(self.model).count()

    def salvar(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def deletar(self, obj: ModelType) -> None:
        self.db.delete(obj)
        self.db.commit()