"""Initial migrations

Revision ID: fd5ee6bde1c9
Revises: 
Create Date: 2024-11-22 14:13:09.481435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd5ee6bde1c9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('spy_cats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('years_of_experience', sa.Integer(), nullable=False),
    sa.Column('breed', sa.String(), nullable=False),
    sa.Column('salary', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_spy_cats_id'), 'spy_cats', ['id'], unique=False)
    op.create_table('missions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cat_id', sa.Integer(), nullable=True),
    sa.Column('is_complete', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['cat_id'], ['spy_cats.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_missions_id'), 'missions', ['id'], unique=False)
    op.create_table('targets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mission_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('notes', sa.String(), nullable=True),
    sa.Column('is_complete', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['mission_id'], ['missions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_targets_id'), 'targets', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_targets_id'), table_name='targets')
    op.drop_table('targets')
    op.drop_index(op.f('ix_missions_id'), table_name='missions')
    op.drop_table('missions')
    op.drop_index(op.f('ix_spy_cats_id'), table_name='spy_cats')
    op.drop_table('spy_cats')
    # ### end Alembic commands ###
