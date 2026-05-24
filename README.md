# client-management-pipefy-integration

Esta é uma API desenvolvida em Python com **FastAPI** para o gerenciamento de clientes, cálculo de prioridade patrimonial e integração simulada com o **Pipefy** através de mutations GraphQL. O projeto conta com persistência local em SQLite, controle de idempotência para webhooks e uma suíte completa de testes automatizados com Pytest.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **FastAPI** (Framework Web)
* **SQLAlchemy** (ORM para persistência de dados)
* **Pydantic** (Validação de dados e Schemas)
* **Pytest & Pytest-Cov** (Testes automatizados e relatório de cobertura)
* **SQLite** (Banco de dados local)

---

## 🚀 Como Executar o Projeto Localmente

### 1. Preparação do Ambiente
```bash
# Criar o ambiente virtual
python -m venv .venv

# Ativar o ambiente virtual (Windows)
.venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Execução
```bash
# Iniciar o servidor
uvicorn api.main:app --reload

# Executar os testes
pytest --cov=api --cov-report=term-missing
```

---

## 📑 Exemplos de Requisição (curl)

### Fluxo 1: Criar Cliente (`POST /clientes`)
Este endpoint valida os dados obrigatórios, persiste o cliente no banco de dados local com o status inicial "Aguardando Análise" (com prioridade inicial `null`) e gera o payload exato da mutation GraphQL `createCard` simulando o envio para o Pipefy.

```bash
curl -X POST "[http://127.0.0.1:8000/clientes](http://127.0.0.1:8000/clientes)" \
     -H "Content-Type: application/json" \
     -d "{\"cliente_nome\": \"João Silva\", \"cliente_email\": \"joao.silva@example.com\", \"tipo_solicitacao\": \"Atualização cadastral\", \"valor_patrimonio\": 250000}"
```

### Fluxo 2: Atualização de Card via Webhook (`POST /webhooks/pipefy/card-updated`)
Este endpoint simula a resposta enviada pelo Pipefy. Ele busca o cliente pelo e-mail, aplica a regra de negócio baseada no patrimônio investido, monta a mutation GraphQL `updateCardField` real e atualiza o banco local para o status "Processado".

```bash
curl -X POST "[http://127.0.0.1:8000/webhooks/pipefy/card-updated](http://127.0.0.1:8000/webhooks/pipefy/card-updated)" \
     -H "Content-Type: application/json" \
     -d "{\"event_id\": \"evt_123\", \"card_id\": \"card_456\", \"cliente_email\": \"joao.silva@example.com\", \"timestamp\": \"2026-05-18T12:00:00Z\"}"
```

---

## ☁️ Visão de Produção (Arquitetura Escalável na AWS)

Para elevar esta aplicação do ambiente de desenvolvimento local para uma estrutura robusta de produção capaz de suportar milhões de requisições na AWS, eu iria propor o seguinte desenho de arquitetura serverless:

* **Porta de Entrada (AWS API Gateway):** Funciona como o ponto de entrada único para os clientes e webhooks externos do Pipefy. Ele gerencia rotas HTTPS, lida com autenticação e possibilita a configuração de Throttling / Rate Limiting, impedindo que picos excessivos de requisições ou ataques maliciosos no webhook sobrecarreguem os serviços internos.
* **Processamento Core Serverless (AWS Lambda):** A aplicação FastAPI é empacotada em uma imagem Docker leve (armazenada no AWS ECR) e executada sob demanda no AWS Lambda. Essa abordagem elimina custos com servidores ociosos, escalando de zero a milhares de execuções simultâneas em frações de segundo automaticamente.
* **Persistência Gerenciada (Amazon RDS PostgreSQL):** Substituindo o SQLite local (apropriado apenas para escopo de teste e desenvolvimento), utiliza-se o PostgreSQL altamente disponível através do Amazon RDS com configuração Multi-AZ (Replicação em zonas de disponibilidade distintas), garantindo consistência transacional ACID, failover automático e backups gerenciados.
* **Assincronismo e Resiliência (AWS SQS):** Para que o processamento do webhook não sofra com lentidões ou timeouts causados por indisponibilidade momentânea de APIs de terceiros, o API Gateway pode apenas publicar o payload recebido do webhook em uma fila do AWS SQS. Uma função Lambda especializada consome essa fila em background. Se houver falha, o evento é enviado para uma fila de tentativas (DLQ) sem perder nenhuma informação.
* **Idempotência de Baixa Latência (Amazon DynamoDB):** A tabela de controle de eventos processados (ProcessedEvent) se beneficia amplamente se migrada para o DynamoDB (banco de dados NoSQL chave-valor). A checagem de duplicidade por chave primária (event_id) ocorre na casa de um dígito de milissegundo. Além disso, pode-se ativar a funcionalidade de TTL (Time to Live) do DynamoDB para deletar de forma automática e sem custos os registros de eventos com mais de 30 dias, mantendo a tabela sempre enxuta.
