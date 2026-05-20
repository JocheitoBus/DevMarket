from fastapi import HTTPException, status
from src.interfaces.schemas.user_schema import UserCreate
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.security.password import PasswordService
from src.infrastructure.database.models import UserModel

class RegisterUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, user_data: UserCreate) -> UserModel:
        if self.user_repo.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado."
            )
        
        if self.user_repo.get_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya está en uso."
            )

        hashed_pwd = PasswordService.hash_password(user_data.password)

        return self.user_repo.create(user_data, hashed_password=hashed_pwd)