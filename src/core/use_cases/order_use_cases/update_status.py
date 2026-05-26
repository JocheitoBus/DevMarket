from fastapi import HTTPException, status
from src.infrastructure.repositories.order_repository import OrderRepository
from src.infrastructure.database.models import OrderModel, UserModel

class UpdateOrderStatusUseCase:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    def execute(self, order_id: int, new_status: str, current_user: UserModel) -> OrderModel:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La orden con ID {order_id} no existe."
            )

        # Ajustable a futuras modificaciones con pasarela de pagos o administradores
        if order.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para modificar esta orden."
            )

        if order.status in ["completed", "cancelled"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede modificar el estado de una orden que ya está {order.status}."
            )

        try:
            updated_order = self.order_repo.update_status(new_status, order_id)
            return updated_order
        except Exception as e:
            raise e