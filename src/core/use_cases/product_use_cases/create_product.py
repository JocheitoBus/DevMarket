from fastapi import HTTPException, status
from src.infrastructure.repositories.product_repository import ProductRepository
from src.infrastructure.database.models import ProductModel, UserModel
from src.interfaces.schemas.product_schemas import ProductCreate

class CreateProductUseCase:
    def __init__(self, user_repo: ProductRepository):
        self.user_repo = user_repo

    def execute(self, product_data : ProductCreate, current_user: UserModel) -> ProductModel:
        new_product = self.user_repo.create(product_data, user_id=current_user.id)
        return new_product