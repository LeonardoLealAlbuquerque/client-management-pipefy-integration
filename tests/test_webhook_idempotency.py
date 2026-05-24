from datetime import datetime

def test_webhook_idempotency_real(client):
    email_teste = "cliente@teste.com"
    client.post("/clientes", json={
        "cliente_nome": "João",
        "cliente_email": email_teste,
        "tipo_solicitacao": "assessoria",
        "valor_patrimonio": 300000.0
    })

    payload = {
        "event_id": "EVT_FIXO_123",
        "cliente_email": email_teste,
        "card_id": "card_001",
        "timestamp": datetime.utcnow().isoformat()
    }

    r1 = client.post("/webhooks/pipefy/card-updated", json=payload)
    assert r1.status_code == 200
    assert r1.json()["message"] == "Webhook processado com sucesso"

    r2 = client.post("/webhooks/pipefy/card-updated", json=payload)
    assert r2.status_code == 200
    assert r2.json()["message"] == "Evento já processado anteriormente"