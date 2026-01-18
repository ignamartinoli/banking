"""add currencies and account.currency_id

Revision ID: 198ae5c8ec51
Revises: be9c38b860d2
Create Date: 2026-01-18 18:48:35.978950

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "198ae5c8ec51"
down_revision: Union[str, None] = 'be9c38b860d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "currencies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=3), nullable=False),
    )
    op.create_index("ix_currencies_code", "currencies", ["code"], unique=True)

    # 2) Seed required currencies
    currencies = sa.table(
        "currencies",
        sa.column("id", sa.Integer()),
        sa.column("code", sa.String()),
    )
    op.bulk_insert(
        currencies,
        [
            {"code": "ARS"},
            {"code": "EUR"},
            {"code": "USD"},
        ],
    )

    # 3) Read ARS id (so we can default accounts.currency_id)
    conn = op.get_bind()
    ars_id = conn.execute(
        sa.text("SELECT id FROM currencies WHERE code = 'ARS'")
    ).scalar_one()

    # 4) Add currency_id to accounts as nullable with a server default = ARS id
    #    - server_default allows existing rows to get a value during the ALTER.
    op.add_column(
        "accounts",
        sa.Column(
            "currency_id", sa.Integer(), nullable=True, server_default=str(ars_id)
        ),
    )
    op.create_index(
        "ix_accounts_currency_id", "accounts", ["currency_id"], unique=False
    )

    # 5) Add FK constraint
    op.create_foreign_key(
        "fk_accounts_currency_id_currencies",
        "accounts",
        "currencies",
        ["currency_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # 6) Backfill existing rows explicitly (belt + suspenders)
    conn.execute(
        sa.text("UPDATE accounts SET currency_id = :ars_id WHERE currency_id IS NULL"),
        {"ars_id": ars_id},
    )

    # 7) Make currency_id NOT NULL
    op.alter_column(
        "accounts", "currency_id", existing_type=sa.Integer(), nullable=False
    )

    # Optional: keep default forever (requested) — leaving server_default in place is fine.
    # If you prefer app-level default only, you could drop it:
    # op.alter_column("accounts", "currency_id", server_default=None)


def downgrade() -> None:
    op.drop_constraint(
        "fk_accounts_currency_id_currencies", "accounts", type_="foreignkey"
    )
    op.drop_index("ix_accounts_currency_id", table_name="accounts")
    op.drop_column("accounts", "currency_id")

    op.drop_index("ix_currencies_code", table_name="currencies")
    op.drop_table("currencies")
