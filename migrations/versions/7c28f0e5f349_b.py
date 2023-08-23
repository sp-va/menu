"""b

Revision ID: 7c28f0e5f349
Revises: acb3b49ad631
Create Date: 2023-08-13 10:33:28.184790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c28f0e5f349'
down_revision = 'acb3b49ad631'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dishes', sa.Column('description', sa.String(), nullable=True))
    op.create_index(op.f('ix_dishes_description'), 'dishes', ['description'], unique=False)
    op.add_column('submenus', sa.Column('description', sa.String(), nullable=True))
    op.create_index(op.f('ix_submenus_description'), 'submenus', ['description'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_submenus_description'), table_name='submenus')
    op.drop_column('submenus', 'description')
    op.drop_index(op.f('ix_dishes_description'), table_name='dishes')
    op.drop_column('dishes', 'description')
    # ### end Alembic commands ###
