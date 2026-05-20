from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    title : str = Field(..., min_length=2, max_length=50, description="Nombre del producto")
    description : str = Field(..., min_length=2, max_length=50, description="Descripcion del producto")
    price : float = Field(...,gt=0,description="Precio (Mayor a cero)")

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class Page:
    skip : int = 0
    limit : int = 100

    class Config:
        from_attributes = True