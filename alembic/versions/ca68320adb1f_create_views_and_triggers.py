"""create views and triggers

Revision ID: ca68320adb1f
Revises: 
Create Date: 2025-11-11 12:15:13.399805

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca68320adb1f'
down_revision: Union[str, Sequence[str], None] = '2d5e154c58a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    # ------------------ VIEWS ------------------
    op.execute("""
    CREATE OR REPLACE VIEW v_monthly_delivered_sales AS
    SELECT DATE_FORMAT(o.created_at, '%Y-%m') AS month_key, SUM(o.total) AS total_sales_delivered
    FROM orders o
    WHERE o.status='delivered'
    GROUP BY DATE_FORMAT(o.created_at, '%Y-%m');
    """)

    op.execute("""
    CREATE OR REPLACE VIEW v_investor_principal AS
    SELECT i.id AS investor_id,
           COALESCE(SUM(CASE m.movement_type
                          WHEN 'invest' THEN  m.amount
                          WHEN 'withdraw' THEN -m.amount
                          WHEN 'adjust' THEN   m.amount
                        END), 0.00) AS principal
    FROM investors i
    LEFT JOIN investor_fund_movements m ON m.investor_id=i.id
    GROUP BY i.id;
    """)

    op.execute("""
    CREATE OR REPLACE VIEW v_monthly_loss_penalty AS
    SELECT s.month_key, s.product_id,
           GREATEST(s.closing_stock - 15, 0) AS surplus_units,
           (GREATEST(s.closing_stock - 15, 0) * p.cost_price) AS loss_amount
    FROM inventory_monthly_snapshot s
    JOIN products p ON p.id=s.product_id;
    """)

    op.execute("""
    CREATE OR REPLACE VIEW v_monthly_loss_penalty_sum AS
    SELECT month_key, SUM(loss_amount) AS loss_penalty
    FROM v_monthly_loss_penalty
    GROUP BY month_key;
    """)

    # ------------------ TRIGGER ------------------
    op.execute("""
        CREATE TRIGGER trg_inv_mov_ai
        AFTER INSERT ON inventory_movements
        FOR EACH ROW
        BEGIN
            DECLARE delta INT;
            IF NEW.movement_type = 'in' THEN
                SET delta = NEW.quantity;
            ELSEIF NEW.movement_type = 'out' THEN
                SET delta = -NEW.quantity;
            ELSE
                SET delta = NEW.quantity;
            END IF;

            INSERT INTO inventory_stock (product_id, qty_on_hand)
            VALUES (NEW.product_id, GREATEST(0, delta))
            ON DUPLICATE KEY UPDATE
                qty_on_hand = GREATEST(0, qty_on_hand + delta),
                updated_at = CURRENT_TIMESTAMP;
        END;
        """)


def downgrade():
    # Drop trigger first
    op.execute("DROP TRIGGER IF EXISTS trg_inv_mov_ai;")
    
    # Drop views
    op.execute("DROP VIEW IF EXISTS v_monthly_loss_penalty_sum;")
    op.execute("DROP VIEW IF EXISTS v_monthly_loss_penalty;")
    op.execute("DROP VIEW IF EXISTS v_investor_principal;")
    op.execute("DROP VIEW IF EXISTS v_monthly_delivered_sales;")