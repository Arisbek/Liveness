from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# Revision identifiers, used by Alembic.
revision = '947e37def49f'
down_revision = 'd8a8daac05e0'
branch_labels = None
depends_on = None

def column_exists(table_name, column_name):
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def upgrade() -> None:
    # Add the 'predictions' column to 'frames' table if it doesn't exist
    if not column_exists('frames', 'predictions'):
        op.add_column('frames', sa.Column('predictions', sa.JSON(), nullable=True))

def downgrade() -> None:
    op.drop_column('frames', 'predictions')