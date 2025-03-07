"""Initial migration

Revision ID: 315698c6094d
Revises: 
Create Date: 2025-03-06 01:20:11.371398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '315698c6094d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('player_stats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=False),
    sa.Column('player_name', sa.String(length=100), nullable=False),
    sa.Column('team_name', sa.String(length=50), nullable=False),
    sa.Column('game_id', sa.String(length=20), nullable=False),
    sa.Column('game_date', sa.String(length=20), nullable=False),
    sa.Column('matchup', sa.String(length=50), nullable=False),
    sa.Column('game_result', sa.String(length=10), nullable=False),
    sa.Column('minutes', sa.Float(), nullable=False),
    sa.Column('fgm', sa.Integer(), nullable=False),
    sa.Column('fga', sa.Integer(), nullable=False),
    sa.Column('fg_percentage', sa.Float(), nullable=False),
    sa.Column('three_pm', sa.Integer(), nullable=False),
    sa.Column('three_pa', sa.Integer(), nullable=False),
    sa.Column('three_p_percentage', sa.Float(), nullable=False),
    sa.Column('ftm', sa.Integer(), nullable=False),
    sa.Column('fta', sa.Integer(), nullable=False),
    sa.Column('ft_percentage', sa.Float(), nullable=False),
    sa.Column('oreb', sa.Integer(), nullable=False),
    sa.Column('dreb', sa.Integer(), nullable=False),
    sa.Column('total_rebounds', sa.Integer(), nullable=False),
    sa.Column('assists', sa.Integer(), nullable=False),
    sa.Column('turnovers', sa.Integer(), nullable=False),
    sa.Column('steals', sa.Integer(), nullable=False),
    sa.Column('blocks', sa.Integer(), nullable=False),
    sa.Column('personal_fouls', sa.Integer(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('plus_minus', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('player_stats')
    # ### end Alembic commands ###
