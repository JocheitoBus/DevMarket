from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.infrastructure.database.database import get_db
from src.infrastructure.repositories.user_repository import UserRepository
from src.core.use_cases.login_user import LoginUserUseCase
from src.interfaces.schemas.auth_schema import UserLoginRequest

from src.core.use_cases.login_user import LoginUserUseCase

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(login_data: UserLoginRequest, db: Session = Depends(get_db)):
    """Autenticar un usuario usando correo y contraseña"""
    user_repository = UserRepository(db)
    login_user_use_case = LoginUserUseCase(user_repository)

    return login_user_use_case.execute(login_data)