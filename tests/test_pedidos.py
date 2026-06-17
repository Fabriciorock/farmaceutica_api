def setup_lote_disponivel(client, produto_payload):
    """Helper: cria produto + lote e leva até status disponivel."""
    produto = client.post("/produtos/", json=produto_payload).json()
    lote = client.post("/lotes/", json={
        "produto_id": produto["id"],
        "codigo_lote": "LOT-TEST",
        "data_fabricacao": "2024-01-01",
        "data_validade": "2030-01-01",
        "quantidade_produzida": 100
    }).json()
    client.patch(f"/lotes/{lote['id']}/status", json={"novo_status": "em_analise_qualidade"})
    client.patch(f"/lotes/{lote['id']}/status", json={"novo_status": "aprovado"})
    client.patch(f"/lotes/{lote['id']}/status", json={"novo_status": "disponivel"})
    return produto, lote


def test_confirmar_pedido_sem_itens_invalido(client, cliente_payload):
    """Cenário de borda: pedido vazio não pode ser confirmado."""
    cliente = client.post("/clientes/", json=cliente_payload).json()
    pedido = client.post("/pedidos/", json={"cliente_id": cliente["id"]}).json()
    r = client.patch(f"/pedidos/{pedido['id']}/status", json={"novo_status": "confirmado"})
    assert r.status_code == 422


def test_adicionar_item_lote_indisponivel_rn001(client, produto_payload, cliente_payload):
    """RN-001: lote em em_producao não pode ser adicionado a pedido."""
    produto = client.post("/produtos/", json=produto_payload).json()
    lote = client.post("/lotes/", json={
        "produto_id": produto["id"],
        "codigo_lote": "LOT-INDISP",
        "data_fabricacao": "2024-01-01",
        "data_validade": "2030-01-01",
        "quantidade_produzida": 100
    }).json()
    cliente = client.post("/clientes/", json=cliente_payload).json()
    pedido = client.post("/pedidos/", json={"cliente_id": cliente["id"]}).json()
    r = client.post(f"/pedidos/{pedido['id']}/itens", json={
        "lote_id": lote["id"],
        "quantidade": 10
    })
    assert r.status_code == 422


def test_pedido_fluxo_completo_valido(client, produto_payload, cliente_payload):
    """Fluxo feliz: criar pedido, adicionar item, confirmar."""
    produto, lote = setup_lote_disponivel(client, produto_payload)
    cliente = client.post("/clientes/", json=cliente_payload).json()
    pedido = client.post("/pedidos/", json={"cliente_id": cliente["id"]}).json()
    r_item = client.post(f"/pedidos/{pedido['id']}/itens", json={
        "lote_id": lote["id"],
        "quantidade": 10
    })
    assert r_item.status_code == 201
    r_confirmar = client.patch(f"/pedidos/{pedido['id']}/status", json={"novo_status": "confirmado"})
    assert r_confirmar.status_code == 200
    assert r_confirmar.json()["status"] == "confirmado"


def test_pedido_estado_terminal_rn006(client, produto_payload, cliente_payload):
    """RN-006: pedido cancelado não aceita novos itens."""
    produto, lote = setup_lote_disponivel(client, produto_payload)
    cliente = client.post("/clientes/", json=cliente_payload).json()
    pedido = client.post("/pedidos/", json={"cliente_id": cliente["id"]}).json()
    client.patch(f"/pedidos/{pedido['id']}/status", json={"novo_status": "cancelado"})
    r = client.post(f"/pedidos/{pedido['id']}/itens", json={
        "lote_id": lote["id"],
        "quantidade": 5
    })
    assert r.status_code == 409


def test_saldo_lote_atualizado_apos_venda(client, produto_payload, cliente_payload):
    """RN-004: saldo do lote deve diminuir após venda."""
    produto, lote = setup_lote_disponivel(client, produto_payload)
    cliente = client.post("/clientes/", json=cliente_payload).json()
    pedido = client.post("/pedidos/", json={"cliente_id": cliente["id"]}).json()
    client.post(f"/pedidos/{pedido['id']}/itens", json={
        "lote_id": lote["id"],
        "quantidade": 30
    })
    r = client.get(f"/lotes/{lote['id']}/saldo")
    assert r.json()["saldo_disponivel"] == 70