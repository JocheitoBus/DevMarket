from sqlalchemy.orm import Session
from src.infrastructure.database.models import OrderModel, OrderItemModel
from src.infrastructure.repositories.product_repository import ProductRepository
from src.interfaces.schemas.order_schema import OrderCreate

class OrderRepository:
    def __init__(self, db: Session, product_repository: ProductRepository):
        self.db = db
        self.product_repo = product_repository

    def create_order(self, order_data: OrderCreate, user_id: int) -> OrderModel:
        """
        Registra una orden completa en la base de datos calculando los precios reales
        y manejando todo dentro de una transacción segura.
        """
        try:
            db_order = OrderModel(
                user_id=user_id,
                total_price=0.0,
                status="pending"
            )


            self.db.add(db_order)
            self.db.flush() 

            running_total = 0.0

            for item in order_data.items:
                product = self.product_repo.get_by_id(item.product_id)

                if not product:
                    raise ValueError(f"El producto con ID {item.product_id} no existe en el catálogo.")

                running_total += product.price * item.quantity

                db_item = OrderItemModel(
                    order_id=db_order.id,
                    product_id=product.id,
                    price_at_purchase=product.price,
                    quantity=item.quantity
                )
                self.db.add(db_item)

            db_order.total_price = running_total
            self.db.commit()
            self.db.refresh(db_order)
            return db_order
        
        except Exception as e:
            self.db.rollback()
            raise e