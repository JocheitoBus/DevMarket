from fastapi import HTTPException, status
from src.infrastructure.security.password import PasswordService
from src.infrastructure.security.jwt_service import JWTService
from src.infrastructure.repositories.user_repository import UserRepository
from src.interfaces.schemas.auth_schema import UserLoginRequest

class LoginUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, login_data: UserLoginRequest) -> dict:
        user = self.user_repo.get_by_email(login_data.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos"
            )

        is_valid = PasswordService.verify_password(login_data.password, user.password_hash)
        
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos"
            )

        token_data = {"sub": str(user.id)}
        access_token = JWTService.create_access_token(data=token_data)

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }