from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
import calendar
from app.database import get_db
from app.models.maintenance import MaintenanceInvoice
from app.models.payment import Payment
from app.models.complaint import Complaint
from app.models.visitor import Visitor
from app.models.user import User
from app.auth.deps import get_current_user

router = APIRouter()


@router.get("/admin")
def admin_dashboard(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    sid = user.society_id
    if not sid:
        return {
            "total_collected": 0, "total_pending": 0, "pending_count": 0,
            "total_complaints": 0, "open_complaints": 0, "in_progress_complaints": 0,
            "resolved_complaints": 0, "total_residents": 0, "active_visitors": 0,
            "monthly_data": [], "complaints_data": [],
        }

    # Total collections (scoped to society)
    total_collected = db.query(func.sum(Payment.amount)).join(MaintenanceInvoice).filter(
        MaintenanceInvoice.society_id == sid
    ).scalar() or 0

    # Pending dues
    pending_invoices = db.query(MaintenanceInvoice).filter(
        MaintenanceInvoice.society_id == sid,
        MaintenanceInvoice.status.in_(["pending", "overdue"])
    ).all()
    total_pending = sum(inv.total_amount for inv in pending_invoices)
    pending_count = len(pending_invoices)

    # Complaints summary
    total_complaints = db.query(func.count(Complaint.id)).filter(Complaint.society_id == sid).scalar() or 0
    open_complaints = db.query(func.count(Complaint.id)).filter(
        Complaint.society_id == sid, Complaint.status == "open"
    ).scalar() or 0
    in_progress = db.query(func.count(Complaint.id)).filter(
        Complaint.society_id == sid, Complaint.status == "in_progress"
    ).scalar() or 0
    resolved = db.query(func.count(Complaint.id)).filter(
        Complaint.society_id == sid, Complaint.status == "resolved"
    ).scalar() or 0

    # Total residents
    total_residents = db.query(func.count(User.id)).filter(
        User.society_id == sid, User.role == "resident", User.is_active == True
    ).scalar() or 0

    # Active visitors
    active_visitors = db.query(func.count(Visitor.id)).filter(
        Visitor.society_id == sid, Visitor.status.in_(["pending", "approved"])
    ).scalar() or 0

    # Monthly collection data (last 6 months)
    monthly_data = []
    current = date.today()
    for i in range(5, -1, -1):
        m = current.month - i
        y = current.year
        while m <= 0:
            m += 12
            y -= 1
        month_total = db.query(func.sum(Payment.amount)).join(MaintenanceInvoice).filter(
            MaintenanceInvoice.society_id == sid,
            MaintenanceInvoice.month == m,
            MaintenanceInvoice.year == y,
        ).scalar() or 0
        month_pending = db.query(func.sum(MaintenanceInvoice.total_amount)).filter(
            MaintenanceInvoice.society_id == sid,
            MaintenanceInvoice.month == m,
            MaintenanceInvoice.year == y,
            MaintenanceInvoice.status.in_(["pending", "overdue"]),
        ).scalar() or 0
        monthly_data.append({
            "month": calendar.month_abbr[m],
            "collected": round(month_total, 2),
            "pending": round(month_pending, 2),
        })

    return {
        "total_collected": round(total_collected, 2),
        "total_pending": round(total_pending, 2),
        "pending_count": pending_count,
        "total_complaints": total_complaints,
        "open_complaints": open_complaints,
        "in_progress_complaints": in_progress,
        "resolved_complaints": resolved,
        "total_residents": total_residents,
        "active_visitors": active_visitors,
        "monthly_data": monthly_data,
        "complaints_data": [
            {"name": "Open", "value": open_complaints},
            {"name": "In Progress", "value": in_progress},
            {"name": "Resolved", "value": resolved},
        ],
    }


@router.get("/resident")
def resident_dashboard(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # My invoices
    my_invoices = db.query(MaintenanceInvoice).filter(
        MaintenanceInvoice.flat_id == user.flat_id
    ).order_by(MaintenanceInvoice.created_at.desc()).limit(10).all() if user.flat_id else []

    # My payments
    my_payments = db.query(Payment).filter(
        Payment.user_id == user.id
    ).order_by(Payment.payment_date.desc()).limit(10).all()

    # My complaints
    my_complaints = db.query(Complaint).filter(
        Complaint.user_id == user.id
    ).order_by(Complaint.created_at.desc()).limit(10).all()

    pending_amount = sum(inv.total_amount for inv in my_invoices if inv.status in ("pending", "overdue"))
    paid_amount = sum(p.amount for p in my_payments)

    return {
        "pending_amount": round(pending_amount, 2),
        "total_paid": round(paid_amount, 2),
        "pending_bills": len([i for i in my_invoices if i.status in ("pending", "overdue")]),
        "open_complaints": len([c for c in my_complaints if c.status != "resolved"]),
        "recent_invoices": [
            {"id": i.id, "month": i.month, "year": i.year, "amount": i.total_amount, "status": i.status}
            for i in my_invoices
        ],
        "recent_payments": [
            {"id": p.id, "amount": p.amount, "date": str(p.payment_date), "method": p.payment_method}
            for p in my_payments
        ],
        "recent_complaints": [
            {"id": c.id, "title": c.title, "status": c.status, "date": str(c.created_at)}
            for c in my_complaints
        ],
    }
