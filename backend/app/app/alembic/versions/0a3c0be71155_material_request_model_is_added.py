"""material request model is added

Revision ID: 0a3c0be71155
Revises: 2d8dc49a846c
Create Date: 2024-09-23 11:33:44.509714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a3c0be71155'
down_revision: Union[str, None] = '2d8dc49a846c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('material',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('material_name', sa.String(length=100), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_material_id'), 'material', ['id'], unique=False)
    op.create_table('material_request',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('units', sa.Integer(), nullable=False),
    sa.Column('material_id', sa.Integer(), nullable=False),
    sa.Column('ticket_id', sa.Integer(), nullable=True),
    sa.Column('emp_id', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['material_id'], ['material.id'], ),
    sa.ForeignKeyConstraint(['ticket_id'], ['ticket.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_material_request_id'), 'material_request', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_material_request_id'), table_name='material_request')
    op.drop_table('material_request')
    op.drop_index(op.f('ix_material_id'), table_name='material')
    op.drop_table('material')
    # ### end Alembic commands ###
