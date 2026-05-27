from fastapi import HTTPException, status
from typing import List
from src.infrastructure.repositories.order_repository import OrderRepository
from src.infrastructure.database.models import OrderModel, UserModel

class GetOrdersUseCase:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    def execute(self, user_id: int, current_user: UserModel) -> List[OrderModel]:
        if user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver esta informacion"
            )
        
        orders = self.order_repo.get_by_user(user_id=user_id)
        return orders