from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# Revision identifiers, used by Alembic.
revision = 'd8a8daac05e0'
down_revision = None
branch_labels = None
depends_on = None

def table_exists(table_name):
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    return table_name in inspector.get_table_names()

def upgrade() -> None:
    # Check if the 'services' table already exists
    if not table_exists('services'):
        op.create_table(
            'services',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('owner', sa.String(), nullable=False),
            sa.Column('password', sa.String(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('password')
        )
        op.create_index(op.f('ix_services_id'), 'services', ['id'], unique=False)
        op.create_index(op.f('ix_services_owner'), 'services', ['owner'], unique=True)

    # Check if the 'frames' table already exists
    if not table_exists('frames'):
        op.create_table(
            'frames',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('owner_id', sa.Integer(), nullable=False),
            sa.Column('frame', sa.String(), nullable=False),
            sa.Column('time_created', sa.TIMESTAMP(), nullable=False),
            sa.ForeignKeyConstraint(['owner_id'], ['services.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_frames_id'), 'frames', ['id'], unique=False)
        op.create_index(op.f('ix_frames_owner_id'), 'frames', ['owner_id'], unique=False)

    # Check if the 'logs' table already exists
    if not table_exists('logs'):
        op.create_table(
            'logs',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('method', sa.String(), nullable=False),
            sa.Column('url', sa.Text(), nullable=False),
            sa.Column('ip_address', sa.String(), nullable=False),
            sa.Column('owner_id', sa.Integer(), nullable=True),
            sa.Column('request', sa.String(), nullable=True),
            sa.Column('response', sa.String(), nullable=True),
            sa.ForeignKeyConstraint(['owner_id'], ['services.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_logs_id'), 'logs', ['id'], unique=False)
        op.create_index(op.f('ix_logs_owner_id'), 'logs', ['owner_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_logs_owner_id'), table_name='logs')
    op.drop_index(op.f('ix_logs_id'), table_name='logs')
    op.drop_table('logs')
    op.drop_index(op.f('ix_frames_owner_id'), table_name='frames')
    op.drop_index(op.f('ix_frames_id'), table_name='frames')
    op.drop_table('frames')
    op.drop_index(op.f('ix_services_owner'), table_name='services')
    op.drop_index(op.f('ix_services_id'), table_name='services')
    op.drop_table('services')