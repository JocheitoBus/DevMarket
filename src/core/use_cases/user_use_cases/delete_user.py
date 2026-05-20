from fastapi import HTTPException, status
from src.interfaces.schemas.user_schema import UserDelete
from src.infrastructure.security.password import PasswordService
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.database.models import UserModel

class DeleteUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self,current_user: UserModel, user_id: int, user_delete: UserDelete):
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
        
        if user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para eliminar esta cuenta."
            )
        
        self.user_repo.delete_user(user)

