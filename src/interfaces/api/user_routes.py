from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.infrastructure.database.database import get_db
from src.interfaces.schemas.user_schema import *
from src.infrastructure.repositories.user_repository import UserRepository
from src.core.use_cases.user_use_cases.register_user import RegisterUserUseCase
from src.core.use_cases.user_use_cases.get_user import GetUserUseCase
from src.core.use_cases.user_use_cases.update_user import UpdateUserUseCase
from src.core.use_cases.user_use_cases.delete_user import DeleteUserUseCase
from src.interfaces.middlewares.auth_bearer import get_current_user
from src.infrastructure.database.models import UserModel

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Endpoint para registrar un nuevo usuario en la plataforma."""
    user_repository = UserRepository(db)
    register_use_case = RegisterUserUseCase(user_repository)
    new_user = register_use_case.execute(user_data)
    return new_user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Obtiene los detalles de un usuario específico por su ID."""
    user_repository = UserRepository(db)
    get_user_use_case = GetUserUseCase(user_repository)
    
    return get_user_use_case.execute(user_id)

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    update_data: UserUpdate, 
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    """Actualiza la informacion de un usuario especifico por su ID con campos opcionales"""
    user_repository = UserRepository(db)
    update_user_use_case = UpdateUserUseCase(user_repository)

    return update_user_use_case.execute(user_id, current_user, update_data)

@router.post("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, user_password: UserDelete, 
    current_user: UserModel = Depends(get_current_user),  
    db: Session = Depends(get_db)
    ):
    """Eliminar un usuario utilizando la contraseña"""
    user_repository = UserRepository(db)
    delete_user_use_case = DeleteUserUseCase(user_repository)

    return delete_user_use_case.execute(current_user,user_id,user_password)
