import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from src.infrastructure.database.database import SessionLocal, engine
from src.infrastructure.database.models import UserModel, ProductModel
from src.infrastructure.database.models import OrderModel, OrderItemModel

from src.infrastructure.security.password import PasswordService 

def clean_database(db: Session):
    """Limpia las tablas en el orden correcto para evitar conflictos de llaves foráneas."""
    print("🧹 Limpiando base de datos existente...")
    db.query(OrderItemModel).delete()
    db.query(OrderModel).delete()
    db.query(ProductModel).delete()
    db.query(UserModel).delete()
    db.commit()

def seed_data():
    db = SessionLocal()
    try:
        clean_database(db)
        print("Insertando datos de prueba ...")

        password_plana = "DevMarket2026"
        PasswordService.hash_password = (password_plana)

        vendedor_1 = UserModel(
            username="jose_dev",
            email="jose@devmarket.com",
            password_hash=PasswordService.hash_password
        )
        vendedor_2 = UserModel(
            username="maria_baker",
            email="maria@bakery.com",
            password_hash=PasswordService.hash_password
        )
        comprador = UserModel(
            username="test_buyer",
            email="buyer@test.com",
            password_hash=PasswordService.hash_password
        )

        db.add_all([vendedor_1, vendedor_2, comprador])
        db.flush()

        productos = [
            ProductModel(
                title="API Backend FastAPI Template",
                description="Estructura limpia E2E lista para producción con JWT y Docker.",
                price=49.99,
                user_id=vendedor_1.id
            ),
            ProductModel(
                title="Plugin de Autenticación Avanzada",
                description="Módulo listo para conectar con proveedores OAuth2 (Google/GitHub).",
                price=19.50,
                user_id=vendedor_1.id
            ),
            ProductModel(
                title="E-commerce Frontend en React",
                description="Dashboard completo para administración de tiendas virtuales.",
                price=89.99,
                user_id=vendedor_2.id
            ),
            ProductModel(
                title="Script de Automatización de Tareas",
                description="Script optimizado para backups automáticos en AWS S3.",
                price=15.00,
                user_id=vendedor_2.id
            )
        ]

        db.add_all(productos)
        db.commit()

        print("\n=======================================================")
        print(" ¡Base de datos poblada con éxito!")
        print("=======================================================")
        print(f" Credenciales comunes para todos los usuarios:")
        print(f"   Password: {password_plana}\n")
        print(f" Usuarios creados:")
        print(f"   - {vendedor_1.username} ({vendedor_1.email}) [Vendedor]")
        print(f"   - {vendedor_2.username} ({vendedor_2.email}) [Vendedor]")
        print(f"   - {comprador.username} ({comprador.email}) [Comprador]")
        print(f"\n Productos creados: {len(productos)} servicios en catálogo.")
        print("=======================================================\n")

    except Exception as e:
        print(f" Error al ejecutar el seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()