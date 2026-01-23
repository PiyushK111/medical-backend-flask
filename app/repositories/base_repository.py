from typing import List, Optional, Type, TypeVar
from app.models.base import db

T = TypeVar("T", bound=db.Model)

class BaseRepository:
    def __init__(self, model: Type[T]):
        self.model = model

    def get_all(self) -> List[T]:
        """Fetch all records."""
        return db.session.execute(db.select(self.model)).scalars().all()

    def get_by_id(self, id: int) -> Optional[T]:
        """Fetch a record by ID."""
        return db.session.get(self.model, id)

    def create(self, **kwargs) -> T:
        """Create a new record."""
        instance = self.model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    def update(self, instance: T, **kwargs) -> T:
        """Update an existing record."""
        for key, value in kwargs.items():
            setattr(instance, key, value)
        db.session.commit()
        return instance

    def delete(self, instance: T) -> None:
        """Delete a record."""
        db.session.delete(instance)
        db.session.commit()
