"""Create admin and event tables

Revision ID: cc2614ea0ed0
Revises: 
Create Date: 2024-08-16 16:54:51.155556

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc2614ea0ed0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'admin',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, nullable=True),
        sa.Column('password', sa.String, nullable=True)
    )

    op.create_table(
        'event',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('az_title', sa.String, nullable=True),
        sa.Column('en_title', sa.String, nullable=True),
        sa.Column('az_content', sa.String, nullable=True),
        sa.Column('en_content', sa.String, nullable=True),
        sa.Column('image', sa.String, nullable=True)
    )

    op.create_table(
        'form_submission',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('data', sa.JSON, nullable=True)
    )

    op.create_table(
        'gallery_image',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('image_url', sa.String, nullable=True)
    )

def downgrade() -> None:
    op.drop_table('event')
    op.drop_table('admin')
    op.drop_table('gallery_image')
    op.drop_table('form_submission')
