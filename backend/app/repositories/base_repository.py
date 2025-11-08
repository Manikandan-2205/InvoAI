from sqlalchemy.orm import Session

class BaseRepository:
    """
    Generic repository base class to handle DB session and common operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def add(self, entity):
        self.db.add(entity)
        return entity

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def refresh(self, entity):
        self.db.refresh(entity)
        return entity
