"""Create the initial SoilWise schema explicitly.

Revision ID: 0001_initial
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=120), nullable=False, server_default=""),
        sa.Column("preferred_language", sa.String(length=5), nullable=False, server_default="en"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "analyses",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("field_name", sa.String(length=120), nullable=False, server_default="My field"),
        sa.Column("image_path", sa.String(length=500), nullable=True),
        sa.Column("nitrogen", sa.Float(), nullable=False),
        sa.Column("phosphorus", sa.Float(), nullable=False),
        sa.Column("potassium", sa.Float(), nullable=False),
        sa.Column("ph", sa.Float(), nullable=False),
        sa.Column("organic_matter", sa.Float(), nullable=False),
        sa.Column("moisture", sa.Float(), nullable=False),
        sa.Column("health_score", sa.Integer(), nullable=False),
        sa.Column("diagnosis", sa.JSON(), nullable=False),
        sa.Column("recommendations", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_analyses_user_id", "analyses", ["user_id"], unique=False)
    op.create_index("ix_analyses_user_created", "analyses", ["user_id", "created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_analyses_user_created", table_name="analyses")
    op.drop_index("ix_analyses_user_id", table_name="analyses")
    op.drop_table("analyses")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
