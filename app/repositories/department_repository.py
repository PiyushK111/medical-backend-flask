from typing import Optional
from app.models.department import Department
from app.repositories.base_repository import BaseRepository
from app.models.base import db

class DepartmentRepository(BaseRepository):
    def __init__(self):
        super().__init__(Department)

    def get_by_name(self, name: str) -> Optional[Department]:
        """Fetch a department by name."""
        return db.session.execute(
            db.select(Department).where(Department.name == name)
        ).scalar_one_or_none()
