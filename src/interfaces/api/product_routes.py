from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from typing import List
from src.infrastructure.database.database import get_db
from src.interfaces.middlewares.auth_bearer import get_current_user
from src.infrastructure.database.models import ProductModel, UserModel
from src.interfaces.schemas.product_schemas import ProductResponse, ProductCreate
from src.infrastructure.repositories.product_repository import ProductRepository

# CASOS DE USO
from src.core.use_cases.product_use_cases.create_product import CreateProductUseCase
from src.core.use_cases.product_use_cases.get_product import GetProductUseCase

router = APIRouter(prefix="/product", tags=["Products"])

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate, 
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user),
    ):
    """Endpoint para registrar un nuevo producto en la plataforma."""
    product_repository = ProductRepository(db)
    create_product_use_case = CreateProductUseCase(product_repository)
    new_product = create_product_use_case.execute(product_data,current_user.id)
    
    return new_product

@router.get("/",response_model=List[ProductResponse], status_code=status.HTTP_200_OK)
def get_all_product(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtiene una lista con todos los productos con ID entre skip y limit (Paginado)"""

    product_repository = ProductRepository(db)
    get_product_use_case = GetProductUseCase(product_repository)

    return get_product_use_case.all_execute(skip=skip,limit=limit)

@router.get("/search",response_model=List[ProductResponse], status_code=status.HTTP_200_OK)
def get_by_title(title: str, skip:int = 0, limit:int = 100, db: Session = Depends(get_db)):
    """Obtiene una lista de productos que contengan 'title' en su titulo (Paginado)"""

    product_repository = ProductRepository(db)
    get_product_use_case = GetProductUseCase(product_repository)

    return get_product_use_case.by_title_execute(title=title,skip=skip,limit=limit)


@router.get("/{product_id}",response_model=ProductResponse, status_code=status.HTTP_200_OK)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """Obtiene los detalles de un producto por su ID"""

    product_repository = ProductRepository(db)
    get_product_use_case = GetProductUseCase(product_repository)
    
    product = get_product_use_case.by_id_execute(product_id)

    return product
