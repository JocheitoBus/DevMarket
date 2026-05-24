from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from typing import List
from src.infrastructure.database.database import get_db
from src.interfaces.middlewares.auth_bearer import get_current_user
from src.infrastructure.database.models import UserModel
from src.interfaces.schemas.product_schemas import ProductResponse, ProductCreate, ProductUpdate
from src.infrastructure.repositories.product_repository import ProductRepository

# CASOS DE USO
from src.core.use_cases.product_use_cases.create_product import CreateProductUseCase
from src.core.use_cases.product_use_cases.get_product import GetProductUseCase
from src.core.use_cases.product_use_cases.delete_product import DeleteProductUseCase
from src.core.use_cases.product_use_cases.update_product import UpdateProductUseCase

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
    new_product = create_product_use_case.execute(product_data=product_data,current_user=current_user)
    
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

@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    update_data: ProductUpdate, 
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    """Actualiza la informacion de un usuario especifico por su ID con campos opcionales"""
    user_repository = ProductRepository(db)
    update_product_use_case = UpdateProductUseCase(user_repository)

    return update_product_use_case.execute(product_id, current_user, update_data)

@router.post("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int, 
    current_user: UserModel = Depends(get_current_user),  
    db: Session = Depends(get_db)
    ):
    """Eliminar un usuario utilizando la contraseña"""
    product_repository = ProductRepository(db)
    delete_product_use_case = DeleteProductUseCase(product_repository)

    return delete_product_use_case.execute(current_user=current_user,product_id=product_id)
