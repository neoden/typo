"""comments

Revision ID: e23a09521e5a
Revises: d0ff8a3810ea
Create Date: 2016-02-15 23:47:06.083941

"""

# revision identifiers, used by Alembic.
revision = 'e23a09521e5a'
down_revision = 'd0ff8a3810ea'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('path', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('text', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_author_id'), 'comments', ['author_id'], unique=False)
    op.create_index(op.f('ix_comments_post_id'), 'comments', ['post_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comments_post_id'), table_name='comments')
    op.drop_index(op.f('ix_comments_author_id'), table_name='comments')
    op.drop_table('comments')
    ### end Alembic commands ###