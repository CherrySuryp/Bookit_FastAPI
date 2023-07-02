"""init2

Revision ID: c71e6b13564d
Revises: be899599eabb
Create Date: 2023-06-27 15:43:20.654206

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c71e6b13564d'
down_revision = 'be899599eabb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hotels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('service', sa.JSON(), nullable=True),
    sa.Column('rooms_quantity', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hotel_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('services', sa.JSON(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('date_from', sa.Date(), nullable=False),
    sa.Column('date_to', sa.Date(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('total_cost', sa.Integer(), sa.Computed('(date_to - date_from) * price', ), nullable=True),
    sa.Column('total_days', sa.Integer(), sa.Computed('(date_to - date_from)', ), nullable=True),
    sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('booking')
    op.drop_table('room')
    op.drop_table('user')
    op.drop_table('hotel')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hotel',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('hotel_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('location', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('service', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('rooms_quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('image_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='hotel_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('user_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('room',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('room_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('hotel_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('services', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('image_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['hotel_id'], ['hotel.id'], name='room_hotel_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='room_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('booking',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('room_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('date_from', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('date_to', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('total_cost', sa.INTEGER(), sa.Computed('((date_to - date_from) * price)', persisted=True), autoincrement=False, nullable=True),
    sa.Column('total_days', sa.INTEGER(), sa.Computed('(date_to - date_from)', persisted=True), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['room_id'], ['room.id'], name='booking_room_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='booking_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='booking_pkey')
    )
    op.drop_table('bookings')
    op.drop_table('rooms')
    op.drop_table('users')
    op.drop_table('hotels')
    # ### end Alembic commands ###
