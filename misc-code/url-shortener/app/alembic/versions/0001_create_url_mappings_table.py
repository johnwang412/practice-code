"""Create url_mappings table

Revision ID: 0001
Revises: 
Create Date: 2025-01-07 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create url_mappings table
    op.create_table('url_mappings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('original_url', sa.String(length=2048), nullable=False),
        sa.Column('short_code', sa.String(length=8), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_url_mappings_id'), 'url_mappings', ['id'], unique=False)
    op.create_index(op.f('ix_url_mappings_short_code'), 'url_mappings', ['short_code'], unique=True)
    op.create_index('idx_short_code', 'url_mappings', ['short_code'], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_short_code', table_name='url_mappings')
    op.drop_index(op.f('ix_url_mappings_short_code'), table_name='url_mappings')
    op.drop_index(op.f('ix_url_mappings_id'), table_name='url_mappings')
    
    # Drop table
    op.drop_table('url_mappings')
