from fastapi import HTTPException, status
from typing import List
from src.infrastructure.repositories.product_repository import ProductRepository
from src.infrastructure.database.models import ProductModel

class GetProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def by_id_execute(self, product_id: int) -> ProductModel:
        product = self.product_repo.get_by_id(product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {product_id} no encontrado"
            )
        
        return product
    
    def all_execute(self, skip:int = 0, limit:int = 100):
        product_list = self.product_repo.get_all(skip=skip,limit=limit)
        return product_list

    def by_title_execute(self, title: str, skip:int = 0, limit:int = 100) -> List[ProductModel]:
        clean_title = title.strip()
        product_list = self.product_repo.get_by_title(title=clean_title,skip=skip,limit=limit)

        if not product_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No hay coincidencias para {title}"
            )

        return product_list