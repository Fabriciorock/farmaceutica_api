import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import get_db
from app.core.config import settings

engine_test = create_engine(settings.DATABASE_URL)
SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    db = SessionTest()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def limpar_banco():
    """Limpa todas as tabelas antes de cada teste — banco isolado."""
    db = SessionTest()
    try:
        db.execute(text("""
            TRUNCATE TABLE recall_lote, recalls, itens_pedido, pedidos,
            controles_qualidade, lotes, produtos, clientes
            RESTART IDENTITY CASCADE
        """))
        db.commit()
    finally:
        db.close()
    yield


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── Fixtures de dados reutilizáveis ───────────────────────────────────────────

@pytest.fixture
def produto_payload():
    return {
        "nome": "Dipirona 500mg",
        "categoria": "medicamento_comum",
        "fabricante": "FarmaLab",
        "preco_unitario": "10.50",
        "requer_autorizacao": False
    }


@pytest.fixture
def produto_controlado_payload():
    return {
        "nome": "Ritalina 10mg",
        "categoria": "medicamento_controlado",
        "fabricante": "FarmaLab",
        "preco_unitario": "25.00",
        "requer_autorizacao": True
    }


@pytest.fixture
def cliente_payload():
    return {
        "razao_social": "Farmácia Central Ltda",
        "cnpj": "12.345.678/0001-90",
        "tipo": "farmacia",
        "autorizado_controlados": False
    }


@pytest.fixture
def cliente_autorizado_payload():
    return {
        "razao_social": "Hospital São Lucas",
        "cnpj": "98.765.432/0001-10",
        "tipo": "hospital",
        "autorizado_controlados": True,
        "validade_autorizacao": "2030-12-31"
    }