from fastapi import FastAPI
from api.routes import clientes
from api.routes import webhooks
from api.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mundo Invest API")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do Mundo Invest está online!"}

app.include_router(clientes.router)
app.include_router(webhooks.router)