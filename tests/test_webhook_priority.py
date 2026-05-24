from datetime import datetime

def test_prioridade_alta_quando_patrimonio_maior_igual_200k(client):
    """Testa se patrimônio >= 200.000 resulta em prioridade_alta"""
    
    client.post("/clientes", json={
        "cliente_nome": "Cliente Teste Alta",
        "cliente_email": "alta@teste.com",
        "tipo_solicitacao": "Atualização cadastral",
        "valor_patrimonio": 200000.0
    })

    payload = {
        "event_id": "EVT_PRIORIDADE_ALTA",
        "cliente_email": "alta@teste.com",
        "card_id": "card_alta",
        "timestamp": datetime.utcnow().isoformat()
    }

    response = client.post("/webhooks/pipefy/card-updated", json=payload)
    
    assert response.status_code == 200
    assert response.json()["prioridade"] == "prioridade_alta"


def test_prioridade_normal_quando_patrimonio_menor_200k(client):
    """Testa se patrimônio < 200.000 resulta em prioridade_normal"""
    
    client.post("/clientes", json={
        "cliente_nome": "Cliente Teste Normal",
        "cliente_email": "normal@teste.com",
        "tipo_solicitacao": "Atualização cadastral",
        "valor_patrimonio": 199999.0
    })

    payload = {
        "event_id": "EVT_PRIORIDADE_NORMAL",
        "cliente_email": "normal@teste.com",
        "card_id": "card_normal",
        "timestamp": datetime.utcnow().isoformat()
    }

    response = client.post("/webhooks/pipefy/card-updated", json=payload)
    
    assert response.status_code == 200
    assert response.json()["prioridade"] == "prioridade_normal"