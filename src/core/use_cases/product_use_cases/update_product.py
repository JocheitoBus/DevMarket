from fastapi import HTTPException, status
from src.infrastructure.repositories.product_repository import ProductRepository
from src.interfaces.schemas.product_schemas import ProductUpdate
from src.infrastructure.database.models import UserModel, ProductModel


class UpdateProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self, product_id: int, current_user: UserModel, update_data: ProductUpdate) -> ProductModel:
        product = self.product_repo.get_by_id(product_id=product_id)
        data_dict = update_data.model_dump(exclude_unset=True)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= f"Producto con ID: {product_id} no existe."
            )
        
        if product.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permitido editar este producto."
            )
        
        return self.product_repo.update(db_product=product,update_data=data_dict)