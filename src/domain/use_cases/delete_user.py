from fastapi import HTTPException, status
from src.domain.schemas.user_schema import UserDelete
from src.core.security.password import PasswordService
from src.infrastructure.repositories.user_repository import UserRepository

class DeleteUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int, user_delete: UserDelete):
        user = self.user_repo.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado."
            )

        if not PasswordService.verify_password(user_delete.password,user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Contraseña incorrecta."
            )
        
        self.user_repo.delete_user(user)
