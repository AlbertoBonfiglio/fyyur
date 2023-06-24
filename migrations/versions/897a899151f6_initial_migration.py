"""Initial Migration

Revision ID: 897a899151f6
Revises: 
Create Date: 2023-06-25 09:12:35.884039

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '897a899151f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Artist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=False),
    sa.Column('state', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=36), nullable=False),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('genres', postgresql.ARRAY(sa.String(length=24)), nullable=True),
    sa.Column('website', sa.String(length=120), nullable=False),
    sa.Column('seeking_venue', sa.Boolean(), nullable=False),
    sa.Column('seeking_description', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_Artist_city'), ['city'], unique=False)
        batch_op.create_index(batch_op.f('ix_Artist_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_Artist_state'), ['state'], unique=False)

    op.create_table('Venue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=False),
    sa.Column('state', sa.String(length=120), nullable=False),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=36), nullable=False),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('genres', postgresql.ARRAY(sa.String(length=24)), nullable=True),
    sa.Column('website', sa.String(length=120), nullable=False),
    sa.Column('seeking_talent', sa.Boolean(), nullable=False),
    sa.Column('seeking_description', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_Venue_city'), ['city'], unique=False)
        batch_op.create_index(batch_op.f('ix_Venue_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_Venue_state'), ['state'], unique=False)

    op.create_table('Show',
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('venue_id', 'artist_id', 'start_time')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Show')
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_Venue_state'))
        batch_op.drop_index(batch_op.f('ix_Venue_name'))
        batch_op.drop_index(batch_op.f('ix_Venue_city'))

    op.drop_table('Venue')
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_Artist_state'))
        batch_op.drop_index(batch_op.f('ix_Artist_name'))
        batch_op.drop_index(batch_op.f('ix_Artist_city'))

    op.drop_table('Artist')
    # ### end Alembic commands ###