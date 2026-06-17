from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class PaginacaoParams(BaseModel):
    """Parametros de paginação reutilizaveis em todos os endpoints de listagem"""
    pagina: int = 1
    por_pagina: int = 10


class RespostaPaginada(BaseModel, Generic[T]):
    """envelope generico de resposta paginada"""
    itens: list[T]
    total: int
    pagina: int
    por_pagina: int
    paginas: int