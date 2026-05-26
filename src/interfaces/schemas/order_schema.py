from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from typing import Literal

class OrderItemCreate(BaseModel):
    product_id: int = Field(..., description="ID del producto que se va a comprar")
    quantity: int = Field(default=1, gt=0, description="Cantidad de unidades (mínimo 1)")


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_at_purchase: float

    model_config = {
        "from_attributes": True
    }

class OrderCreate(BaseModel):
    items: List[OrderItemCreate] = Field(..., min_items=1, description="Lista de productos en el carrito")


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse]

    model_config = {
        "from_attributes": True
    }

class OrderUpdateStatus(BaseModel):
    status: Literal["completed", "cancelled"] = Field(
        ..., 
        description="El nuevo estado de la orden: 'completed' o 'cancelled'"
    )