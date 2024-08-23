"""created menu item table

Revision ID: 014a2118d78b
Revises: cc2614ea0ed0
Create Date: 2024-08-22 15:57:24.056039

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '014a2118d78b'
down_revision: Union[str, None] = 'cc2614ea0ed0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'menu',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('data', sa.JSON, nullable=True)
    )


def downgrade() -> None:
    op.drop_table('menu')
