from fastapi import FastAPI
from src.infrastructure.database.database import engine, Base
from src.interfaces.api.user_routes import router as user_router
from src.interfaces.api.auth_routes import router as auth_router
from src.interfaces.api.product_routes import router as product_router

from src.infrastructure.database.models import UserModel, ProductModel

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevMarket API",
    description="API RESTful para un marketplace de desarrolladores",
    version="1.0.0"
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(product_router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "¡Empingao Asere! El servidor esta pinchando."
    }