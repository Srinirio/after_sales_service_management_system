"""user and destination models are added

Revision ID: efb1547e92e2
Revises: d4342cfd916d
Create Date: 2024-09-19 10:19:00.613556

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'efb1547e92e2'
down_revision: Union[str, None] = 'd4342cfd916d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('destination',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('destination_name', sa.String(length=40), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_destination_id'), 'destination', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.String(length=20), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('phone_number', sa.String(length=10), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('destination_id', sa.Integer(), nullable=True),
    sa.Column('report_to', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['destination_id'], ['destination.id'], ),
    sa.ForeignKeyConstraint(['report_to'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_index(op.f('ix_destination_id'), table_name='destination')
    op.drop_table('destination')
    # ### end Alembic commands ###
