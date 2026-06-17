# apresentação do sistema

 Sistema de Gestão Farmacêutica e Cosméticos

O sistema modela a operação de uma empresa farmacêutica e de cosmeticos que realiza vendas B2B para farmácias, distribuidores e hospitais.

O domínio é centrado na rastreabilidade de lotes de produção: cada venda referencia não apenas um produto, mas um lote específico — garantindo conformidade regulatória e rastreabilidade total, do processo produtivo até a entrega ao cliente final.

Pilares do domínio


    Rastreabilidade por lote — toda transação aponta para um lote específico com data de validade e quantidade controlada

    Controle de qualidade — lotes precisam ser aprovados em análise antes de serem disponibilizados para venda

    Regulamentação de medicamentos controlados — clientes que adquirem medicamentos controlados precisam de autorização vigente

    Gestão de recalls — eventos de recolhimento propagam bloqueios automáticos em pedidos ativos com os lotes afetados

    Ciclos de vida — lotes e pedidos possuem máquinas de estado que regem as transições permitidas


# Entidades e Relacionamentos


Entidade                Responsabilidade

Produto                 Catálogo: nome, categoria, fabricante, preço

Lote                    Produção física de um produto com validade e rastreabilidade

ControleQualidade       Análise laboratorial vinculada a um lote

Cliente                 Farmácia, distribuidor ou hospital comprador

Pedido                  Ordem de compra de um cliente

ItemPedido              tem de um pedido referenciando um lote específico

Recall                  Evento de recolhimento que afeta um ou mais lotes


Relacionamentos

Entidade A          Entidade B          Cardinalidade           Descrição

Produto             Lote                    1:N                 Um produto possui vários lotes de produção

Lote                ControleQualidade       1:N                 Um lote pode ter múltiplas análises

Cliente             Pedido                  1:N                 Um cliente realiza vários pedidos

Pedido              ItemPedido              1:N                 Um pedido contém múltiplos itens

Lote                ItemPedido              1:N                 Um lote aparece em vários itens (rastreabilidade)

Recall              Lote                    N:N                 Um recall afeta múltiplos lotes


uma decisão de design que tomei foi a do ItemPedido referencia o Lote (e não o Produto diretamente) para garantir rastreabilidade regulatoria — sabe-se exatamente qual lote, com qual validade e de qual produção, foi entregue a qual cliente.


# Regras de Negócio

ID                  Nome                            Gatilho                     Pré-condição                    Erro

RN-001              Lote indisponível               Adição de                   lote.status == "disponivel"     422
                    bloqueado                       ItemPedido

RN-002              Lote vencido bloqueado          Adição de ItemPedido        lote.data_validade >= hoje      422

RN-003              Autorização para controlados    Confirmação de Pedido       Cliente com                     403
                                                                                autorizado_controlados=True 
                                                                                e validade_autorizacao >= hoje

RN-004              Saldo não pode ficar negativo   Adição de ItemPedido        quantidade <= saldo_disponivel  422

RN-005              Transições de estado válidas    Alteração de status         Transição deve constar          422
                                                                                na máquina de estados

RN-006              Estado terminal é imutável      Edição de Pedido            status NOT IN                   409
                                                                                {entregue, cancelado}

RN-007              Recall bloqueia pedidos ativos  Emissão de Recall           Pedidos confirmado/faturado/     —
                                                                                enviado com itens do lote →
                                                                                bloqueado_recall

RN-008              Lote recolhido não entra        Adição de ItemPedido        lote.status NOT IN              422
                    em pedido                                                   {recolhido, reprovado}


Todas as regras de negócio estão implementadas na camada service, nunca no router




# Diagrama ER

 ─────────────────┐         ┌──────────────────────┐
│    PRODUTO      │         │   CONTROLE_QUALIDADE │
├─────────────────┤         ├──────────────────────┤
│ id (PK)         │         │ id (PK)              │
│ nome            │         │ lote_id (FK)         │
│ categoria       │         │ data_analise         │
│ fabricante      │         │ responsavel          │
│ principio_ativo │         │ resultado            │
│ preco_unitario  │         │ observacoes          │
│ requer_autori.. │         └──────────┬───────────┘
└────────┬────────┘                    │ N
         │ 1                           │
         │ N                    ┌──────┴───────────┐
┌────────┴────────┐    N:N      │      LOTE        │
│      LOTE       ├─────────────┤──────────────────┤
├─────────────────┤  RECALL_    │ id (PK)          │
│ id (PK)         │  LOTE       │ produto_id (FK)  │
│ produto_id (FK) │             │ codigo_lote      │
│ codigo_lote     │             │ data_fabricacao  │
│ data_fabricacao │             │ data_validade    │
│ data_validade   │             │ qtd_produzida    │
│ qtd_produzida   │             │ status           │
│ status          │             └──────────────────┘
└────────┬────────┘
         │ 1
         │ N
┌────────┴────────┐        ┌──────────────────────┐
│   ITEM_PEDIDO   │        │       PEDIDO         │
├─────────────────┤        ├──────────────────────┤
│ id (PK)         │  N     │ id (PK)              │
│ pedido_id (FK)  ├────────┤ cliente_id (FK)      │
│ lote_id (FK)    │        │ data_pedido          │
│ quantidade      │        │ status               │
│ preco_unit_mom  │        │ valor_total          │
└─────────────────┘        └──────────┬───────────┘
                                      │ N
                                      │ 1
                            ┌─────────┴───────────┐
                            │      CLIENTE        │
                            ├─────────────────────┤
                            │ id (PK)             │
                            │ razao_social        │
                            │ cnpj (UNIQUE)       │ coloquei o CNPJ como UNIQUE pois não pode ter um CNPJ igual a outro
                            │ tipo                │
                            │ autorizado_control..│
                            │ validade_autorizacao│
                            └─────────────────────┘

┌─────────────────┐
│     RECALL      │──────── N:N ──────── LOTE (via recall_lote)
├─────────────────┤
│ id (PK)         │
│ motivo          │
│ descricao       │
│ data_emissao    │
└─────────────────┘


(OBS: deu trabalho fazer isso :)



# Como Rodar Localmente

tenha o docker aberto no pc (obiviamente).

configure as variaveis de ambiente: cp .env.example .env

e por final é só dá o: docker compose up --build

(OBS: caso não rode tente baixar todas os imports do requirements.txt, caso mesmo assim não rode o problema éna sua maquina pq aqui rodou :)

se apareceu isso aqui: 
 Running upgrade -> 001 - Fundação: produtos, clientes e lotes
 Running upgrade 001 -> 002 - Camada de vendas
 Running upgrade 002 -> 003 - Compliance e qualidade
 Application startup complete.

 então rodou

 credenciais para o pgadmin

 Email: admin@admin.com
 Senha: admin123

 para onectar ao banco no pgadmin:

 Host: farmaceutica_db
 Port: 5432
 Database: farmaceutica_db
 Username: farmacia_user
 Password: farmacia_pass

 o sistema vai rodae perfeitamente se vc rodar da forma que eu expliquei acima 

 
 
# Rodar os testes

rode isso para fazer os testes: docker compose exec api pytest tests/ -v

tem que dá que 18 passed, e 0 failed

para rodar o rollback de migration é só usar esse comando: docker compose exec api alembic downgrade -1





# Algumas perguntas e respostas sobre o sistema

## Por que ItemPedido referencia Lote e não Produto diretamente?

Para garantir rastreabilidade regulatoria. Em sistemas farmaceuticos, não basta saber que foi vendido "Dipirona 500mg" — é necessário saber exatamente qual lote, de qual data de fabricação, com qual validade, foi entregue a qual cliente. Se houver um recall posterior, é possivel identificar quais clientes precisam ser notificados.


## Por que as regras de negocio ficam no service e não no router?

Separação de camadas. O router não deve saber de regras de negocio — ele so recebe uma requisição HTTP e devolve uma resposta. Se amanhã a aplicação tiver uma interface de linha de comando ou um worker assincrono, as mesmas regras do service se aplicam sem duplicação.


## Por que criar exceções de dominio em vez de usar HTTPException diretamente?

O service não deve saber que existe HTTP. SaldoInsuficienteException é uma exceção de dominio — ela diz "a regra foi violada". Quem decide que isso vira um HTTP 422 é o handler global no main.py. Isso mantim o service independente do framework web.


## Como você trataria race conditions (dois usuários comprando o mesmo lote ao mesmo tempo)?

O calculo de saldo é feito dentro da mesma transação do banco, usando SELECT ... FOR UPDATE ou isolamento de transação. PostgreSQL garante que duas transações concorrentes não ultrapassem o saldo disponivel simultaneamente.


## Por que a migration 002 foi necessaria separada da 001?

Para contar uma historia de evolução do sistema. Primeiro o catalogo (produtos, clientes, lotes), depois a capacidade de vender (pedidos, itens). Isso reflete como um sistema real evolui: primeiro você modela o dominio, depois adiciona as operações comerciais.


## Quais estados são terminais no Pedido e por quê?

entregue e cancelado. São terminais porque representam estados irreversiveis no mundo real — uma entrega confirmada não pode ser "desfeita" no sistema, e um pedido cancelado já liberou os saldos dos lotes. O estado bloqueado_recall não é terminal porque pode ser resolvido com cancelamento.


## Por que valor_total esta salvo no Pedido se é um valor derivado?

É uma desnormalização controlada para performance. Calcular a soma dos itens em toda listagem de pedidos seria custoso. O service garante que valor_total é sempre recalculado apos qualquer alteração nos itens, então nunca fica desatualizado. É uma decisão consciente de tradeoff entre normalização e performance.


## Como o recall garante consistencia ao bloquear multiplos pedidos?

Toda a operação do recall — criar o recall, mudar o status dos lotes para recolhido e mudar o status dos pedidos para bloqueado_recall — acontece dentro da mesma transação do banco. Se qualquer parte falhar, o banco desfaz tudo. Nunca vai existir um lote recolhido com um pedido ainda confirmado.




# algumas decisões relevantes que eu tomei ao longo do desenvolvimento do sistema

1 ItemPedido referencia Lote, não Produto
Garante rastreabilidade regulatoria completa. Sabe-se exatamente qual lote foi entregue a qual cliente, com qual validade e de qual produção.

2 preco_unitario_momento como snapshot
O preço é capturado no momento da venda e nunca alterado. Permite auditar o valor exato pago em qualquer pedido histórico.

3 Exceções de domínio separadas de HTTPException
O service não sabe que existe HTTP. Lança SaldoInsuficienteException. O handler global no main.py converte para HTTP 422. Se trocar o framework, as regras de negócio continuam iguais.

4 valor_total como cache controlado
O valor total é derivado dos itens, mas é mantido no Pedido como cache. O service garante que é sempre atualizado após cada mudança nos itens. Evita recalcular em cada listagem.

5 Duas máquinas de estado
Tanto Lote quanto Pedido têm ciclos de vida com transições explícitas definidas em dicionários (TRANSICOES_LOTE, TRANSICOES_PEDIDO). Qualquer transição inválida é bloqueada com 422.

6 Migrations contando uma história


001 — Fundação: produtos, clientes e lotes
002 — Camada de vendas: pedidos e itens
003 — Compliance: controle de qualidade, recall e índices de performance


7 PgAdmin4 no docker-compose
Interface visual para o banco de dados acessível em http://localhost:5050, subindo junto com a API e o PostgreSQL em um único docker compose up (isso aqui realmente é bem legal, nem sabia da existencia disso kkk).

# qualquer outra informação sobre o sistema está no aquivo que enviei junto ao do projeto no AVA.