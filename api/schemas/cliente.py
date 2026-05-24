from pydantic import BaseModel, EmailStr
from typing import Optional

class ClienteBase(BaseModel):
    cliente_nome: str
    cliente_email: EmailStr
    tipo_solicitacao: str
    valor_patrimonio: float

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int
    status: str
    prioridade: Optional[str] = None
    
    class Config:
        from_attributes = True