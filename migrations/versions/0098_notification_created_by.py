"""add created_by col to notification

Revision ID: 0098_notification_created_by
Revises: 0097_notnull_inbound_provider
Create Date: 2017-06-13 10:53:25.032202

"""

# revision identifiers, used by Alembic.
revision = '0098_notification_created_by'
down_revision = '0097_notnull_inbound_provider'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.add_column('notifications', sa.Column('created_by_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'notifications', 'users', ['created_by_id'], ['id'])


def downgrade():
    op.drop_constraint(None, 'notifications', type_='foreignkey')
    op.drop_column('notifications', 'created_by_id')
