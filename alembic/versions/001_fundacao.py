"""001 - Fundação: produtos, clientes e lotes

Revision ID: 001
Revises: 
Create Date: 2024-01-01
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'produtos',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('nome', sa.String(200), nullable=False),
        sa.Column('categoria', sa.String(50), nullable=False),
        sa.Column('fabricante', sa.String(200), nullable=False),
        sa.Column('principio_ativo', sa.String(300), nullable=True),
        sa.Column('preco_unitario', sa.Numeric(12, 2), nullable=False),
        sa.Column('requer_autorizacao', sa.Boolean, nullable=False, server_default='false'),
    )
    op.create_table(
        'clientes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('razao_social', sa.String(300), nullable=False),
        sa.Column('cnpj', sa.String(18), nullable=False, unique=True),
        sa.Column('tipo', sa.String(30), nullable=False),
        sa.Column('autorizado_controlados', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('validade_autorizacao', sa.Date, nullable=True),
    )
    op.create_table(
        'lotes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('produto_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('produtos.id'), nullable=False),
        sa.Column('codigo_lote', sa.String(100), nullable=False, unique=True),
        sa.Column('data_fabricacao', sa.Date, nullable=False),
        sa.Column('data_validade', sa.Date, nullable=False),
        sa.Column('quantidade_produzida', sa.Integer, nullable=False),
        sa.Column('status', sa.String(30), nullable=False, server_default='em_producao'),
    )
    op.create_index('ix_lotes_produto_id', 'lotes', ['produto_id'])
    op.create_index('ix_lotes_status', 'lotes', ['status'])


def downgrade() -> None:
    op.drop_index('ix_lotes_status', 'lotes')
    op.drop_index('ix_lotes_produto_id', 'lotes')
    op.drop_table('lotes')
    op.drop_table('clientes')
    op.drop_table('produtos')