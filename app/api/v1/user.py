from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from core.db import get_db
from core.security import get_current_user
from crud import user
from models.user import User
from schemas.user import UserInpt, UserOut

router = APIRouter(prefix="/v1/users", tags=["Users"])


@router.post("/", response_model=UserOut)
def create_user(request: UserInpt, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get("/{id}", response_model=UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserInpt = Depends(get_current_user),
):
    if id != current_user.id and current_user.role == User.UserRole.ADMIN.value:
        raise HTTPException(status_code=403, detail="Not authorized to show this user's data")

    user = user.show_user(id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not available",
        )
    return user


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(
    id: int,
    request: UserInpt,
    db: Session = Depends(get_db),
    current_user: UserInpt = Depends(get_current_user),
):
    if id != current_user.id and current_user.role == User.UserRole.ADMIN.value:
        raise HTTPException(status_code=403, detail="Not authorized to update this user's data")

    user = user.show_user(id, db)

    try:
        return user.update_user(id, request, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserInpt = Depends(get_current_user),
):
    if id != current_user.id and current_user.role == User.UserRole.ADMIN.value:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user's data")

    return user.destroy(id, db)
