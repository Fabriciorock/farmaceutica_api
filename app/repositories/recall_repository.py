from sqlalchemy.orm import Session
from app.models.recall import Recall
from app.repositories.base import BaseRepository


class RecallRepository(BaseRepository[Recall]):

    def __init__(self, db: Session):
        super().__init__(Recall, db)