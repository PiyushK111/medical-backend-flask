from typing import Optional, Tuple
from app.repositories.user_repository import UserRepository
from app.security.utils import hash_password, verify_password
from app.security.jwt import generate_token
from app.models.user import User, UserRole
import logging

logger = logging.getLogger(__name__)

class AuthService:
    """
    Service for handling user authentication and registration.
    """
    def __init__(self):
        self.user_repository = UserRepository()

    def register_user(self, data: dict) -> Tuple[bool, str, Optional[User]]:
        """
        Registers a new user.
        
        Args:
            data (dict): User registration data (email, password, etc.)
            
        Returns:
            Tuple[bool, str, Optional[User]]: (success, message, user_obj)
        """
        logger.debug(f"Attempting to register user: {data.get('email')}")
        existing_user = self.user_repository.get_by_email(data['email'])
        if existing_user:
            logger.warning(f"Registration failed: User already exists ({data.get('email')})")
            return False, "User already exists", None

        # Hash password before saving
        data['password_hash'] = hash_password(data.pop('password'))
        
        # Default role is MEMBER if not specified
        if 'role' not in data:
            data['role'] = UserRole.MEMBER
            
        new_user = self.user_repository.create(**data)
        logger.info(f"User registered successfully: ID {new_user.id}")
        return True, "User created successfully", new_user

    def login_user(self, data: dict) -> Tuple[bool, str, Optional[str]]:
        """
        Authenticates a user.
        
        Args:
            data (dict): Login credentials (email, password)
            
        Returns:
            Tuple[bool, str, Optional[str]]: (success, message, token)
        """
        user = self.user_repository.get_by_email(data['email'])
        
        if not user:
            logger.warning(f"Login failed: User not found ({data.get('email')})")
            return False, "Invalid credentials", None
            
        if not verify_password(user.password_hash, data['password']):
            logger.warning(f"Login failed: Invalid password ({data.get('email')})")
            return False, "Invalid credentials", None
            
        token = generate_token(user.id, user.role.value)
        logger.info(f"User logged in: ID {user.id}")
        return True, "Login successful", token
