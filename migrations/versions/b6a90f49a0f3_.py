"""empty message

Revision ID: b6a90f49a0f3
Revises: 1de21c9cf196
Create Date: 2023-10-16 01:51:55.446003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6a90f49a0f3'
down_revision = '1de21c9cf196'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('mass', sa.Integer(), nullable=True),
    sa.Column('hair_color', sa.String(length=20), nullable=True),
    sa.Column('skin_color', sa.String(length=20), nullable=True),
    sa.Column('eye_color', sa.String(length=20), nullable=True),
    sa.Column('birth_year', sa.Integer(), nullable=True),
    sa.Column('gender', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('climate', sa.String(length=50), nullable=True),
    sa.Column('terrain', sa.String(length=50), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('diameter', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('starship',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.Column('model', sa.String(length=250), nullable=False),
    sa.Column('manufacturer', sa.String(length=250), nullable=True),
    sa.Column('cost_in_credits', sa.Integer(), nullable=True),
    sa.Column('length', sa.Integer(), nullable=True),
    sa.Column('max_atmosphering_speed', sa.Integer(), nullable=True),
    sa.Column('crew', sa.Integer(), nullable=True),
    sa.Column('passengers', sa.Integer(), nullable=True),
    sa.Column('cargo_capacity', sa.Integer(), nullable=True),
    sa.Column('consumables', sa.String(length=50), nullable=True),
    sa.Column('hyperdrive_rating', sa.Integer(), nullable=True),
    sa.Column('starship_class', sa.String(length=50), nullable=True),
    sa.Column('pilots', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite_character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['character.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite_planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite_starship',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('starship_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['starship_id'], ['starship.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorite_starship')
    op.drop_table('favorite_planet')
    op.drop_table('favorite_character')
    op.drop_table('starship')
    op.drop_table('planet')
    op.drop_table('character')
    # ### end Alembic commands ###
