from fastapi import HTTPException, status
from src.infrastructure.repositories.order_repository import OrderRepository
from src.infrastructure.repositories.product_repository import ProductRepository
from src.infrastructure.database.models import OrderModel, UserModel
from src.interfaces.schemas.order_schema import OrderCreate

class CreateOrderUseCase:
    def __init__(self, order_repo: OrderRepository, product_repo: ProductRepository):
        self.order_repo = order_repo
        self.product_repo = product_repo

    def execute(self, order_data: OrderCreate, current_user: UserModel) -> OrderModel:
        for item in order_data.items:
            product = self.product_repo.get_by_id(item.product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El producto no existe."
                )
            
            owner_id = product.user_id
            if owner_id == current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No puede comprar su propio producto."
                )
        try:
            new_order = self.order_repo.create_order(order_data, user_id=current_user.id)
            return new_order

        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(ve)
            )
            
        except Exception as e:
            raise e