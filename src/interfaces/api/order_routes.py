from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.infrastructure.database.models import UserModel
from src.infrastructure.database.database import get_db
from src.interfaces.schemas.order_schema import OrderCreate, OrderResponse, OrderUpdateStatus
from src.infrastructure.repositories.order_repository import OrderRepository
from src.infrastructure.repositories.product_repository import ProductRepository
from src.interfaces.middlewares.auth_bearer import get_current_user

from src.core.use_cases.order_use_cases.create_order import CreateOrderUseCase
from src.core.use_cases.order_use_cases.update_status import UpdateOrderStatusUseCase
from src.core.use_cases.order_use_cases.get_orders import GetOrdersUseCase

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_new_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Crea un nuevo pedido con los productos del carrito. 
    El ID del comprador se extrae de forma segura del token JWT."""
    
    product_repository = ProductRepository(db)
    order_repository = OrderRepository(db, product_repository=product_repository)
    use_case = CreateOrderUseCase(order_repository,product_repository)
    
    return use_case.execute(order_data=order_data, current_user=current_user)

@router.get("/{user_id}")
def get_orders(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Devuelve una lista de las comprar pasadas de un usuario"""

    product_repository = ProductRepository(db)
    order_repository = OrderRepository(db,product_repository)
    use_case = GetOrdersUseCase(order_repository)

    return use_case.execute(user_id=user_id,current_user=current_user)

@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_data: OrderUpdateStatus,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Actualiza el estado de una orden a 'completed' o 'cancelled'.
    Protegido por JWT. Solo el dueño de la orden puede cambiar su estado."""

    product_repository = ProductRepository(db)
    order_repository = OrderRepository(db,product_repository)
    use_case = UpdateOrderStatusUseCase(order_repository)
    
    return use_case.execute(
        order_id=order_id, 
        new_status=status_data.status, 
        current_user=current_user
    )