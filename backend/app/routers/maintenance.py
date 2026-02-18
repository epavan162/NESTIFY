from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.maintenance import MaintenanceInvoice
from app.models.payment import Payment
from app.models.user import User
from app.schemas.schemas import InvoiceCreate, InvoiceOut, PaymentCreate, PaymentOut
from app.auth.deps import get_current_user, require_role

router = APIRouter()


# --- Invoices ---
@router.get("/invoices", response_model=list[InvoiceOut])
def list_invoices(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role in ("admin", "treasurer") and user.society_id:
        invoices = db.query(MaintenanceInvoice).filter(
            MaintenanceInvoice.society_id == user.society_id
        ).order_by(MaintenanceInvoice.created_at.desc()).all()
    elif user.flat_id:
        invoices = db.query(MaintenanceInvoice).filter(
            MaintenanceInvoice.flat_id == user.flat_id
        ).order_by(MaintenanceInvoice.created_at.desc()).all()
    else:
        invoices = []

    # Auto-apply late fee for overdue invoices
    today = date.today()
    changed = False
    for inv in invoices:
        if inv.status == "pending" and inv.due_date < today:
            inv.status = "overdue"
            if inv.late_fee == 0:
                inv.late_fee = inv.amount * 0.1  # 10% late fee
                inv.total_amount = inv.amount + inv.late_fee
            changed = True
    if changed:
        db.commit()
    return invoices


@router.post("/invoices", response_model=InvoiceOut)
def create_invoice(
    data: InvoiceCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin", "treasurer")),
):
    society_id = data.society_id or user.society_id
    if not society_id:
        raise HTTPException(status_code=400, detail="Society ID required")

    # Parse due_date string to date object
    try:
        due_date_parsed = date.fromisoformat(data.due_date)
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid due_date format. Use YYYY-MM-DD")

    invoice = MaintenanceInvoice(
        society_id=society_id,
        flat_id=data.flat_id,
        amount=data.amount,
        total_amount=data.amount,
        due_date=due_date_parsed,
        month=data.month,
        year=data.year,
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


# --- Payments ---
@router.get("/payments", response_model=list[PaymentOut])
def list_payments(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role in ("admin", "treasurer") and user.society_id:
        return db.query(Payment).join(MaintenanceInvoice).filter(
            MaintenanceInvoice.society_id == user.society_id
        ).order_by(Payment.payment_date.desc()).all()
    return db.query(Payment).filter(Payment.user_id == user.id).order_by(Payment.payment_date.desc()).all()


@router.post("/payments", response_model=PaymentOut)
def record_payment(
    data: PaymentCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    invoice = db.query(MaintenanceInvoice).filter(MaintenanceInvoice.id == data.invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if invoice.status == "paid":
        raise HTTPException(status_code=400, detail="Invoice already paid")
    payment = Payment(
        invoice_id=data.invoice_id,
        user_id=user.id,
        amount=data.amount,
        payment_method=data.payment_method,
        transaction_id=data.transaction_id,
    )
    db.add(payment)
    invoice.status = "paid"
    db.commit()
    db.refresh(payment)
    return payment
