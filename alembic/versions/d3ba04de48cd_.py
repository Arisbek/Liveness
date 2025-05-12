from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# Revision identifiers, used by Alembic.
revision = 'd3ba04de48cd'
down_revision = '947e37def49f'
branch_labels = None
depends_on = None

def column_exists(table_name, column_name):
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def upgrade() -> None:
    # Add the 'time_created' column to 'logs' table if it doesn't exist
    if not column_exists('logs', 'time_created'):
        op.add_column('logs', sa.Column('time_created', sa.TIMESTAMP(), nullable=True))

def downgrade() -> None:
    op.drop_column('logs', 'time_created')