import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def build_create_card_mutation(pipe_id: str, nome: str, email: str, valor_patrimonio: float) -> str:
    """Monta a query para criar um card no Pipefy."""
    mutation = f"""
    mutation {{
      createCard(input: {{pipe_id: "{pipe_id}", fields_attributes: [
        {{field_id: "nome", field_value: "{nome}"}},
        {{field_id: "email", field_value: "{email}"}},
        {{field_id: "valor_patrimonio", field_value: "{valor_patrimonio}"}}
      ]}}) {{ card {{ id }} }}
    }}
    """
    logger.info(f"Gerando mutation de criação: {mutation}")
    return mutation

def build_update_priority_mutation(card_id: str, prioridade: str) -> str:
    """Monta a query para atualizar o campo de prioridade no Pipefy."""
    mutation = f"""
    mutation {{
      updateCardField(input: {{card_id: "{card_id}", field_id: "prioridade", new_value: "{prioridade}"}}) {{
        card {{ id }}
      }}
    }}
    """
    logger.info(f"Gerando mutation de atualização de prioridade: {mutation}")
    return mutation