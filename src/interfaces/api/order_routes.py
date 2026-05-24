from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.infrastructure.database.models import UserModel
from src.infrastructure.database.database import get_db
from src.interfaces.schemas.order_schema import OrderCreate, OrderResponse
from src.infrastructure.repositories.order_repository import OrderRepository
from src.infrastructure.repositories.product_repository import ProductRepository
from src.core.use_cases.order_use_cases.create_order import CreateOrderUseCase
from src.interfaces.middlewares.auth_bearer import get_current_user

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