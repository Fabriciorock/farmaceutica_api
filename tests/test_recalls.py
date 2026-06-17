def setup_pedido_confirmado(client, produto_payload, cliente_payload):
    """Helper: cria um pedido confirmado com lote disponível."""
    produto = client.post("/produtos/", json=produto_payload).json()
    lote = client.post("/lotes/", json={
        "produto_id": produto["id"],
        "codigo_lote": "LOT-RECALL",
        "data_fabricacao": "2024-01-01",
        "data_validade": "2030-01-01",
        "quantidade_produzida": 100
    }).json()
    client.patch(f"/lotes/{lote['id']}/status", json={"novo_status": "em_analise_qualidade"})
    client.patch(f"/lotes/{lote['id']}/status", json={"novo_status": "aprovado"})
    client.patch(f"/lotes/{lote['id']}/status", json={"novo_status": "disponivel"})
    cliente = client.post("/clientes/", json=cliente_payload).json()
    pedido = client.post("/pedidos/", json={"cliente_id": cliente["id"]}).json()
    client.post(f"/pedidos/{pedido['id']}/itens", json={"lote_id": lote["id"], "quantidade": 10})
    client.patch(f"/pedidos/{pedido['id']}/status", json={"novo_status": "confirmado"})
    return lote, pedido


def test_recall_bloqueia_pedidos_ativos_rn007(client, produto_payload, cliente_payload):
    """RN-007: recall deve bloquear pedidos confirmados automaticamente."""
    lote, pedido = setup_pedido_confirmado(client, produto_payload, cliente_payload)
    r = client.post("/recalls/", json={
        "motivo": "Contaminação detectada no lote",
        "lote_ids": [lote["id"]]
    })
    assert r.status_code == 201
    assert pedido["id"] in [str(p) for p in r.json()["pedidos_bloqueados"]]
    r_pedido = client.get(f"/pedidos/{pedido['id']}")
    assert r_pedido.json()["status"] == "bloqueado_recall"


def test_recall_sem_lotes_invalido(client):
    """Recall deve ter pelo menos um lote."""
    r = client.post("/recalls/", json={
        "motivo": "Teste",
        "lote_ids": []
    })
    assert r.status_code == 422


def test_recall_muda_status_lote_para_recolhido(client, produto_payload, cliente_payload):
    """Após recall, lote deve ficar com status recolhido."""
    lote, _ = setup_pedido_confirmado(client, produto_payload, cliente_payload)
    client.post("/recalls/", json={
        "motivo": "Recall teste",
        "lote_ids": [lote["id"]]
    })
    r = client.get(f"/lotes/{lote['id']}")
    assert r.json()["status"] == "recolhido"