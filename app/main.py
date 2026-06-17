from fastapi import FastAPI
from app.core.exceptions import register_exception_handlers
from app.routers import (
    produto_router,
    cliente_router,
    lote_router,
    controle_qualidade_router,
    pedido_router,
    recall_router,
)

app = FastAPI(
    title="Sistema de Gestão Farmacêutica e Cosméticos",
    description="API para rastreabilidade de lotes, controle de qualidade e gestão de pedidos.",
    version="1.0.0",
)

# Registra handlers globais de exceção
register_exception_handlers(app)

# Registra todos os routers
app.include_router(produto_router.router)
app.include_router(cliente_router.router)
app.include_router(lote_router.router)
app.include_router(controle_qualidade_router.router)
app.include_router(pedido_router.router)
app.include_router(recall_router.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API Farmacêutica rodando!"}