from sqlalchemy.orm import Session
from typing import List
from src.infrastructure.database.models import ProductModel
from src.interfaces.schemas.product_schemas import ProductCreate

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, product_id : int) -> ProductModel | None:
        """Busca un producto por su ID único."""
        return self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
    
    def get_by_title(
            self, 
            title : str,
            skip: int = 0,
            limit: int = 100
        ) -> List[ProductModel] | None:
        """Busca productos por su nombre"""
        
        return self.db.query(ProductModel)\
            .filter(ProductModel.title.contains(title))\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def get_by_description(self, product_description : str) -> List[ProductModel] | None:
        """Busca productos por su descripcion"""
        return self.db.query(ProductModel).filter(ProductModel.description == f"%{product_description}%")
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ProductModel]:
        """Devuelve una lista de todos los productos del market con paginación."""
        return self.db.query(ProductModel).offset(skip).limit(limit).all()

    def create(self, product_data: ProductCreate, user_id: int) -> ProductModel:
        """Guarda un nuevo producto en la base de datos asignándole el ID del dueño."""
        db_product = ProductModel(
            title=product_data.title,
            description=product_data.description,
            price=product_data.price,
            user_id=user_id
        )
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def update(self, db_product: ProductModel, update_data: dict) -> ProductModel:
        """Actualiza un producto en la base de datos por su id"""
        for key, value in update_data.items():
            setattr(db_product, key, value)

        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def delete(self, product_id: int) -> bool:
        """Elimina un producto por su ID. Devuelve True si lo borró, False si no existía."""
        product = self.get_by_id(product_id)
        if product:
            self.db.delete(product)
            self.db.commit()
            return True
        return False