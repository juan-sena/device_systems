from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device


def create_loan(db: Session, loan_data):
    loan = Loan(
        user_id=loan_data.user_id,
        device_id=loan_data.device_id,
        status="active"
    )
    device = db.query(Device).filter(Device.id == loan_data.device_id).first()
    device.is_available = False
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


def get_loans(db: Session):
    return db.query(Loan).all()


def get_loan_by_id(db: Session, loan_id: int):
    return db.query(Loan).filter(Loan.id == loan_id).first()


def return_loan(db: Session, loan: Loan):
    loan.status = "returned"
    loan.return_date = datetime.utcnow()
    device = db.query(Device).filter(Device.id == loan.device_id).first()
    device.is_available = True
    db.commit()
    db.refresh(loan)
    return loan


def get_loans_with_details(db: Session):
    return (
        db.query(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .all()
    )


def get_loans_by_user(db: Session, user_id: int):
    return (
        db.query(Loan)
        .filter(Loan.user_id == user_id)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .all()
    )


def get_loans_by_device(db: Session, device_id: int):
    return (
        db.query(Loan)
        .filter(Loan.device_id == device_id)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .all()
    )


def get_loans_filtered(
    db: Session,
    status: str = None,
    user_email: str = None,
    device_type: str = None
):
    query = (
        db.query(Loan)
        .join(Loan.user)
        .join(Loan.device)
        .options(joinedload(Loan.user), joinedload(Loan.device))
    )

    if status:
        query = query.filter(Loan.status == status)
    if user_email:
        query = query.filter(User.email.ilike(user_email))
    if device_type:
        query = query.filter(Device.device_type == device_type)

    return query.all()