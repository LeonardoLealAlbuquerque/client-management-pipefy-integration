def test_create_cliente(client):
    payload = {
        "cliente_nome": "João Silva",
        "cliente_email": "joao@exemplo.com",
        "tipo_solicitacao": "Analise",
        "valor_patrimonio": 250000.0
    }

    response = client.post("/clientes/", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["cliente_nome"] == "João Silva"
    assert data["cliente_email"] == "joao@exemplo.com"
    assert data["status"] == "Aguardando Análise"
    assert "id" in data