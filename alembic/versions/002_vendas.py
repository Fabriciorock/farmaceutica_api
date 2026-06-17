"""002 - Camada de vendas: pedidos e itens de pedido

Revision ID: 002
Revises: 001
Create Date: 2024-01-02
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'pedidos',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('cliente_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('clientes.id'), nullable=False),
        sa.Column('data_pedido', sa.DateTime, nullable=False),
        sa.Column('status', sa.String(30), nullable=False, server_default='rascunho'),
        sa.Column('valor_total', sa.Numeric(14, 2), nullable=False, server_default='0.00'),
    )
    op.create_index('ix_pedidos_cliente_id', 'pedidos', ['cliente_id'])
    op.create_index('ix_pedidos_status', 'pedidos', ['status'])
    op.create_table(
        'itens_pedido',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('pedido_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('pedidos.id'), nullable=False),
        sa.Column('lote_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('lotes.id'), nullable=False),
        sa.Column('quantidade', sa.Integer, nullable=False),
        sa.Column('preco_unitario_momento', sa.Numeric(12, 2), nullable=False),
    )
    op.create_index('ix_itens_pedido_pedido_id', 'itens_pedido', ['pedido_id'])
    op.create_index('ix_itens_pedido_lote_id', 'itens_pedido', ['lote_id'])


def downgrade() -> None:
    op.drop_index('ix_itens_pedido_lote_id', 'itens_pedido')
    op.drop_index('ix_itens_pedido_pedido_id', 'itens_pedido')
    op.drop_table('itens_pedido')
    op.drop_index('ix_pedidos_status', 'pedidos')
    op.drop_index('ix_pedidos_cliente_id', 'pedidos')
    op.drop_table('pedidos')