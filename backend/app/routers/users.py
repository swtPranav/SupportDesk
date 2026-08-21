from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserStatusUpdate
from app.security import hash_password


router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )

    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role=user_data.role,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get(
    "",
    response_model=list[UserResponse],
)
def get_users(
    include_inactive: bool = Query(default=False),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    query = db.query(User)
    if not include_inactive:
        query = query.filter(User.is_active == True)
    return query.order_by(User.id.asc()).all()


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.is_active == True,
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user_status(
    user_id: int,
    user_data: UserStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == current_user.id and not user_data.is_active:
        raise HTTPException(
            status_code=400,
            detail="You cannot deactivate your own account",
        )

    user.is_active = user_data.is_active
    db.commit()
    db.refresh(user)
    return user
