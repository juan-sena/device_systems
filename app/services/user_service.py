from sqlalchemy.orm import Session
from app.models.user_model import User


def create_user(db: Session, user_data):

    user = User(
        name=user_data.name,
        email=user_data.email,
        role=user_data.role,
        is_active=user_data.is_active
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_users(db: Session):

    return db.query(User).all()


def get_user_by_id(
    db: Session,
    user_id: int
):

    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def get_user_by_email(
    db: Session,
    email: str
):

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def update_user(
    db: Session,
    user: User,
    user_data
):

    user.name = user_data.name
    user.email = user_data.email
    user.role = user_data.role
    user.is_active = user_data.is_active

    db.commit()
    db.refresh(user)

    return user


def patch_user(
    db: Session,
    user: User,
    data: dict
):

    for field, value in data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user: User
):

    db.delete(user)
    db.commit()


def get_users_by_role(
    db: Session,
    role: str
):

    return (
        db.query(User)
        .filter(User.role == role)
        .all()
    )


def get_users_by_status(
    db: Session,
    is_active: bool
):

    return (
        db.query(User)
        .filter(User.is_active == is_active)
        .all()
    )


def get_users_ordered_by_name(
    db: Session
):

    return (
        db.query(User)
        .order_by(User.name)
        .all()
    )


def get_users_ordered_by_created_at(
    db: Session
):

    return (
        db.query(User)
        .order_by(User.created_at)
        .all()
    )