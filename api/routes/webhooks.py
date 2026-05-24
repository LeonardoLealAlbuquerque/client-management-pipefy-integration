from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.core.database import get_db
from api.schemas.webhook import WebhookPayload
from api.services.webhook_service import webhook_service

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

@router.post("/pipefy/card-updated")
def handle_pipefy_webhook(payload: WebhookPayload, db: Session = Depends(get_db)):
    resultado = webhook_service(payload, db)
    return resultado