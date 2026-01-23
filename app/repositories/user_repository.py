from typing import Optional
from app.models.user import User
from app.repositories.base_repository import BaseRepository
from app.models.base import db

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email: str) -> Optional[User]:
        """Fetch a user by email."""
        return db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar_one_or_none()
