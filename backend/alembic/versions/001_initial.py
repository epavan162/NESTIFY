"""initial migration

Revision ID: 001_initial
Revises:
Create Date: 2026-02-18
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Societies
    op.create_table('societies',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('address', sa.String(500), nullable=False),
        sa.Column('city', sa.String(100), nullable=False),
        sa.Column('state', sa.String(100), nullable=False),
        sa.Column('pincode', sa.String(10), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )

    # Towers
    op.create_table('towers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('society_id', sa.Integer(), sa.ForeignKey('societies.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('total_floors', sa.Integer(), default=1),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Flats
    op.create_table('flats',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('tower_id', sa.Integer(), sa.ForeignKey('towers.id', ondelete='CASCADE'), nullable=False),
        sa.Column('flat_number', sa.String(20), nullable=False),
        sa.Column('floor', sa.Integer(), default=0),
        sa.Column('area_sqft', sa.Float()),
        sa.Column('flat_type', sa.String(20)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Users
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(255), unique=True),
        sa.Column('phone', sa.String(20), unique=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255)),
        sa.Column('role', sa.String(20), default='resident'),
        sa.Column('society_id', sa.Integer(), sa.ForeignKey('societies.id')),
        sa.Column('flat_id', sa.Integer(), sa.ForeignKey('flats.id')),
        sa.Column('is_owner', sa.Boolean(), default=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('google_id', sa.String(255), unique=True),
        sa.Column('avatar_url', sa.String(500)),
        sa.Column('moved_in_at', sa.DateTime(timezone=True)),
        sa.Column('moved_out_at', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )

    # Maintenance Invoices
    op.create_table('maintenance_invoices',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('society_id', sa.Integer(), sa.ForeignKey('societies.id'), nullable=False),
        sa.Column('flat_id', sa.Integer(), sa.ForeignKey('flats.id'), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('late_fee', sa.Float(), default=0.0),
        sa.Column('total_amount', sa.Float(), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(20), default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )

    # Payments
    op.create_table('payments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('invoice_id', sa.Integer(), sa.ForeignKey('maintenance_invoices.id'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('payment_method', sa.String(50)),
        sa.Column('transaction_id', sa.String(255)),
        sa.Column('payment_date', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Complaints
    op.create_table('complaints',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('society_id', sa.Integer(), sa.ForeignKey('societies.id'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('flat_id', sa.Integer(), sa.ForeignKey('flats.id')),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('image_url', sa.String(500)),
        sa.Column('status', sa.String(20), default='open'),
        sa.Column('priority', sa.String(20), default='medium'),
        sa.Column('assigned_to', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )

    # Visitors
    op.create_table('visitors',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('society_id', sa.Integer(), sa.ForeignKey('societies.id'), nullable=False),
        sa.Column('flat_id', sa.Integer(), sa.ForeignKey('flats.id'), nullable=False),
        sa.Column('visitor_name', sa.String(255), nullable=False),
        sa.Column('visitor_phone', sa.String(20)),
        sa.Column('purpose', sa.String(255)),
        sa.Column('vehicle_number', sa.String(20)),
        sa.Column('entry_time', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('exit_time', sa.DateTime(timezone=True)),
        sa.Column('status', sa.String(20), default='pending'),
        sa.Column('approved_by', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Notices
    op.create_table('notices',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('society_id', sa.Integer(), sa.ForeignKey('societies.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('category', sa.String(50), default='general'),
        sa.Column('created_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )

    # Bookings
    op.create_table('bookings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('society_id', sa.Integer(), sa.ForeignKey('societies.id'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('facility_name', sa.String(100), nullable=False),
        sa.Column('booking_date', sa.Date(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('status', sa.String(20), default='confirmed'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Polls
    op.create_table('polls',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('society_id', sa.Integer(), sa.ForeignKey('societies.id'), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('options', sa.JSON(), nullable=False),
        sa.Column('created_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('expires_at', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Votes
    op.create_table('votes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('poll_id', sa.Integer(), sa.ForeignKey('polls.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('option_index', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Create indexes
    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_users_phone', 'users', ['phone'])


def downgrade() -> None:
    op.drop_table('votes')
    op.drop_table('polls')
    op.drop_table('bookings')
    op.drop_table('notices')
    op.drop_table('visitors')
    op.drop_table('complaints')
    op.drop_table('payments')
    op.drop_table('maintenance_invoices')
    op.drop_table('users')
    op.drop_table('flats')
    op.drop_table('towers')
    op.drop_table('societies')
