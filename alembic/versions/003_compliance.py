"""003 - Camada de compliance: controle de qualidade e recall

Revision ID: 003
Revises: 002
Create Date: 2024-01-03
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'controles_qualidade',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('lote_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('lotes.id'), nullable=False),
        sa.Column('data_analise', sa.DateTime, nullable=False),
        sa.Column('responsavel', sa.String(200), nullable=False),
        sa.Column('resultado', sa.String(20), nullable=False),
        sa.Column('observacoes', sa.Text, nullable=True),
    )
    op.create_index('ix_cq_lote_id', 'controles_qualidade', ['lote_id'])
    op.create_table(
        'recalls',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('motivo', sa.String(500), nullable=False),
        sa.Column('descricao', sa.Text, nullable=True),
        sa.Column('data_emissao', sa.DateTime, nullable=False),
    )
    op.create_table(
        'recall_lote',
        sa.Column('recall_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('recalls.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('lote_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('lotes.id', ondelete='CASCADE'), primary_key=True),
    )
    op.create_index('ix_lotes_data_validade', 'lotes', ['data_validade'])
    op.create_index('ix_pedidos_data_pedido', 'pedidos', ['data_pedido'])


def downgrade() -> None:
    op.drop_index('ix_pedidos_data_pedido', 'pedidos')
    op.drop_index('ix_lotes_data_validade', 'lotes')
    op.drop_table('recall_lote')
    op.drop_table('recalls')
    op.drop_index('ix_cq_lote_id', 'controles_qualidade')
    op.drop_table('controles_qualidade')