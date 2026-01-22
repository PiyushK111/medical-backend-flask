# Users, Roles, Staff inheritance


from enum import Enum as PyEnum
from typing import List, TYPE_CHECKING

from sqlalchemy import String, Boolean, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import db, TimestampMixin


class UserRole(str, PyEnum):
    """
    User roles in the system.

    ADMIN: Full system access - manage users, departments, approve claims
    DOCTOR: Medical professional - manage availability, view appointments
    MEMBER: Patient/customer - book appointments, submit claims
    """
    ADMIN = "admin"
    DOCTOR = "doctor"
    MEMBER = "member"


class User(TimestampMixin, db.Model):
    """
    User model representing all users in the system.

    Uses single-table inheritance - all user types (Admin, Doctor, Member)
    stored in one table with 'role' column to differentiate.

    SECURITY NOTE:
    - password_hash is NEVER exposed via API
    - Use werkzeug's security functions for hashing
    """

    __tablename__ = "users"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Email serves as username - must be unique
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )

    # Hashed password - NEVER store plain text
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # User's display name
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Role determines permissions
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.MEMBER,
        nullable=False
    )

    # Soft delete flag
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<User {self.email} ({self.role.value})>"

    def to_dict(self) -> dict:
        """Convert model to dictionary for API responses."""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role.value,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat()
        }
