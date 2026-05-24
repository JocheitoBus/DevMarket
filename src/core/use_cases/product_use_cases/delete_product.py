from fastapi import HTTPException, status
from src.infrastructure.repositories.product_repository import ProductRepository
from src.infrastructure.database.models import ProductModel, UserModel


class DeleteProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self, product_id: int, current_user: UserModel):
        product = self.product_repo.get_by_id(product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID: {product_id} no existe."
            )

        if product.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permitido eliminar este producto."
            )

        self.product_repo.delete(product_id=product_id)