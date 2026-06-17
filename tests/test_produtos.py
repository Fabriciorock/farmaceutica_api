def test_criar_produto_valido(client, produto_payload):
    r = client.post("/produtos/", json=produto_payload)
    assert r.status_code == 201
    assert r.json()["nome"] == "Dipirona 500mg"
    assert r.json()["categoria"] == "medicamento_comum"


def test_criar_produto_preco_zero_invalido(client, produto_payload):
    produto_payload["preco_unitario"] = "0"
    r = client.post("/produtos/", json=produto_payload)
    assert r.status_code == 422


def test_criar_produto_preco_negativo_invalido(client, produto_payload):
    produto_payload["preco_unitario"] = "-5.00"
    r = client.post("/produtos/", json=produto_payload)
    assert r.status_code == 422


def test_listar_produtos_paginado(client, produto_payload):
    client.post("/produtos/", json=produto_payload)
    r = client.get("/produtos/?pagina=1&por_pagina=10")
    assert r.status_code == 200
    assert r.json()["total"] == 1
    assert len(r.json()["itens"]) == 1


def test_deletar_produto_sem_lotes(client, produto_payload):
    r = client.post("/produtos/", json=produto_payload)
    produto_id = r.json()["id"]
    r = client.delete(f"/produtos/{produto_id}")
    assert r.status_code == 204


def test_buscar_produto_inexistente(client):
    r = client.get("/produtos/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404