"""init

Revision ID: be899599eabb
Revises: 
Create Date: 2023-06-26 01:08:13.897060

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'be899599eabb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hotel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('service', sa.JSON(), nullable=True),
    sa.Column('rooms_quantity', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hotel_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('services', sa.JSON(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['hotel_id'], ['hotel.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('booking',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('date_from', sa.Date(), nullable=False),
    sa.Column('date_to', sa.Date(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('total_cost', sa.Integer(), sa.Computed('(date_to - date_from) * price', ), nullable=True),
    sa.Column('total_days', sa.Integer(), sa.Computed('(date_to - date_from)', ), nullable=True),
    sa.ForeignKeyConstraint(['room_id'], ['room.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('booking')
    op.drop_table('room')
    op.drop_table('user')
    op.drop_table('hotel')
    # ### end Alembic commands ###
