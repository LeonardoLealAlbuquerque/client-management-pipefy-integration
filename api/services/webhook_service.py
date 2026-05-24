from sqlalchemy.orm import Session
from sympy import python
from api.models.processed_event import ProcessedEvent
from api.models.cliente import Cliente
from api.schemas.webhook import WebhookPayload
from api.integrations.pipefy_client import build_update_priority_mutation

def webhook_service(payload: WebhookPayload, db: Session):
    # 1. Idempotência: Verifica se este evento já foi processado
    existing_event = db.query(ProcessedEvent).filter(ProcessedEvent.event_id == payload.event_id).first()
    if existing_event:
        return {"status": "ignored", "message": "Evento já processado anteriormente"}
   
    # 2. Busca o cliente para processar
    cliente = db.query(Cliente).filter(Cliente.cliente_email == payload.cliente_email).first()
    if not cliente:
        return {"status": "error", "message": "Cliente não encontrado"}

    # 3. Lógica de Negócio: Calcular Prioridade
    prioridade = "prioridade_alta" if cliente.valor_patrimonio >= 200000 else "prioridade_normal"

    # 4. Chama a integração (Mock/Log)
    build_update_priority_mutation(payload.card_id, prioridade)

    # 5. Persistir resultados
    cliente.prioridade = prioridade
    cliente.status = "Processado"

    new_event = ProcessedEvent(event_id=payload.event_id)
    db.add(new_event)
    db.commit()
    
    return {"message": "Webhook processado com sucesso", "prioridade": prioridade}