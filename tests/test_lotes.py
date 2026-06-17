import datetime


def criar_produto(client, payload):
    return client.post("/produtos/", json=payload).json()


def test_criar_lote_valido(client, produto_payload):
    produto = criar_produto(client, produto_payload)
    r = client.post("/lotes/", json={
        "produto_id": produto["id"],
        "codigo_lote": "LOT-001",
        "data_fabricacao": "2024-01-01",
        "data_validade": "2026-01-01",
        "quantidade_produzida": 100
    })
    assert r.status_code == 201
    assert r.json()["status"] == "em_producao"
    assert r.json()["codigo_lote"] == "LOT-001"


def test_lote_validade_anterior_fabricacao_invalido(client, produto_payload):
    produto = criar_produto(client, produto_payload)
    r = client.post("/lotes/", json={
        "produto_id": produto["id"],
        "codigo_lote": "LOT-002",
        "data_fabricacao": "2024-06-01",
        "data_validade": "2024-01-01",
        "quantidade_produzida": 100
    })
    assert r.status_code == 422


def test_transicao_status_valida(client, produto_payload):
    produto = criar_produto(client, produto_payload)
    lote = client.post("/lotes/", json={
        "produto_id": produto["id"],
        "codigo_lote": "LOT-003",
        "data_fabricacao": "2024-01-01",
        "data_validade": "2026-01-01",
        "quantidade_produzida": 50
    }).json()
    r = client.patch(f"/lotes/{lote['id']}/status", json={"novo_status": "em_analise_qualidade"})
    assert r.status_code == 200
    assert r.json()["status"] == "em_analise_qualidade"


def test_transicao_status_invalida_rn005(client, produto_payload):
    """RN-005: não é possível ir de em_producao direto para disponivel."""
    produto = criar_produto(client, produto_payload)
    lote = client.post("/lotes/", json={
        "produto_id": produto["id"],
        "codigo_lote": "LOT-004",
        "data_fabricacao": "2024-01-01",
        "data_validade": "2026-01-01",
        "quantidade_produzida": 50
    }).json()
    r = client.patch(f"/lotes/{lote['id']}/status", json={"novo_status": "disponivel"})
    assert r.status_code == 422