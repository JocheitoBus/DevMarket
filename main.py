from fastapi import FastAPI
from src.config.database import engine, Base
from src.infrastructure.database.models import UserModel
from src.infrastructure.api.user_routes import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevMarket API",
    description="API RESTful para un marketplace de desarrolladores",
    version="1.0.0"
)

app.include_router(user_router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "¡Empingao Asere! El servidor esta pinchando."
    }