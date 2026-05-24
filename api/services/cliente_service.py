from sqlalchemy.orm import Session
from api.models.cliente import Cliente
from api.schemas.cliente import ClienteCreate
from api.integrations.pipefy_client import build_create_card_mutation

PIPE_ID = "123456789"

def create_cliente_service(cliente_data: ClienteCreate, db: Session):
    db_cliente = Cliente(**cliente_data.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)

    build_create_card_mutation(
        pipe_id=PIPE_ID,
        nome=db_cliente.cliente_nome,
        email=db_cliente.cliente_email,
        valor_patrimonio=db_cliente.valor_patrimonio
    )

    return db_cliente
