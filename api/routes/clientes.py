from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.core.database import get_db
from api.schemas.cliente import ClienteCreate, Cliente
from api.services.cliente_service import create_cliente_service

router = APIRouter()

@router.post("/clientes/", response_model=Cliente)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    novo_cliente = create_cliente_service(cliente, db)
    return novo_cliente