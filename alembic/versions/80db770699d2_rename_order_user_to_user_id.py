"""rename order user to user_id

Revision ID: 80db770699d2
Revises: 628adec80d8c
Create Date: 2026-03-27 10:00:35.070358

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80db770699d2'
down_revision: Union[str, Sequence[str], None] = '628adec80d8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("orders") as batch_op:
        batch_op.alter_column("user", new_column_name="user_id")


def downgrade() -> None:
    with op.batch_alter_table("orders") as batch_op:
        batch_op.alter_column("user_id", new_column_name="user")
