from fastapi import HTTPException, status
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.database.models import UserModel

class GetUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int) -> UserModel:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado."
            )
        return user