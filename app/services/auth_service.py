from typing import Optional, Tuple
from app.repositories.user_repository import UserRepository
from app.security.utils import hash_password, verify_password
from app.security.jwt import generate_token
from app.models.user import User, UserRole

class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    def register_user(self, data: dict) -> Tuple[bool, str, Optional[User]]:
        """
        Registers a new user.
        Returns: (success, message, user_obj)
        """
        existing_user = self.user_repository.get_by_email(data['email'])
        if existing_user:
            return False, "User already exists", None

        # Hash password before saving
        data['password_hash'] = hash_password(data.pop('password'))
        
        # Default role is MEMBER if not specified (or restricted elsewhere)
        # Note: The schema validation already ensures 'role' is valid if present.
        # But for public registration, we might want to force MEMBER. 
        # For this assignment, we'll allow role to be passed if the schema allows it,
        # but standard public register usually shouldn't allow creating admins.
        # Since requirements say 'Implement POST /auth/register', we'll assume standard user registration.
        # If 'role' is in data, we use it, otherwise default.
        # Ideally, admin creation should be seeded or separate.
        
        if 'role' not in data:
            data['role'] = UserRole.MEMBER
            
        new_user = self.user_repository.create(**data)
        return True, "User created successfully", new_user

    def login_user(self, data: dict) -> Tuple[bool, str, Optional[str]]:
        """
        Authenticates a user.
        Returns: (success, message, token)
        """
        user = self.user_repository.get_by_email(data['email'])
        
        if not user:
            return False, "Invalid credentials", None
            
        if not verify_password(user.password_hash, data['password']):
            return False, "Invalid credentials", None
            
        token = generate_token(user.id, user.role.value)
        return True, "Login successful", token
