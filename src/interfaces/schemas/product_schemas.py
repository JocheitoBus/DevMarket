from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    title : str = Field(..., min_length=2, max_length=50, description="Nombre del producto")
    description : str = Field(..., min_length=2, max_length=300, description="Descripcion del producto")
    price : float = Field(...,gt=0,description="Precio (Mayor a cero)")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    title : Optional[str] = None
    description : Optional[str] = None
    price : Optional[float] = None
    

class ProductResponse(ProductBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True