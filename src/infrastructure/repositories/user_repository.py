from sqlalchemy.orm import Session
from src.infrastructure.database.models import UserModel
from src.interfaces.schemas.user_schema import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> UserModel | None:
        """Busca un usuario por su ID único."""
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_by_email(self, email: str) -> UserModel | None:
        """Busca un usuario en la base de datos por su correo electrónico."""
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    def get_by_username(self, username: str) -> UserModel | None:
        """Busca un usuario en la base de datos por su nombre de usuario."""
        return self.db.query(UserModel).filter(UserModel.username == username).first()

    def create(self, user_data: UserCreate, hashed_password: str) -> UserModel:
        """Inserta un nuevo usuario en la base de datos."""
        db_user = UserModel(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password 
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, db_user: UserModel, update_data: dict) -> UserModel | None:
        """Actualiza un usuario en la base de datos por su id"""
        for key, value in update_data.items():
            setattr(db_user, key, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def delete_user(self, db_user: UserModel) -> None:
        """Elimina un usuario de la base de datos"""
        self.db.delete(db_user)
        self.db.commit()
        