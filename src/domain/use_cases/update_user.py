from fastapi import HTTPException, status
from src.infrastructure.repositories.user_repository import UserRepository
from src.domain.schemas.user_schema import UserUpdate
from src.infrastructure.database.models import UserModel

class UpdateUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int, update_data: UserUpdate) -> UserModel:
        user = self.user_repo.get_by_id(user_id)
        dict_data = update_data.model_dump(exclude_unset=True)
        
        if not dict_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El contenido para actualizar esta vacio."
            )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado."
            )
        #else:
            existing_user = self.user_repo.get_by_id(user_id)
            if "username" in dict_data and existing_user.username == dict_data["username"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Los nombres de usuario antiguo y nuevo son iguales."
                )
            if "email" in dict_data and existing_user.username == dict_data["email"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Las direcciones de correo antigua y nueva son iguales."
                )

        if "email" in dict_data:
            new_email = dict_data["email"]
            existing_user = self.user_repo.get_by_email(new_email)

            if existing_user and existing_user.id != user_id:
                 raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Correo electronico siendo usado por otro usuario."
                )

        return self.user_repo.update(user,dict_data)
