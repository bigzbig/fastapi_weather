from sqlalchemy.orm import Session
from models.user import User
from core.security import Hash
from schemas.user import UserInpt


def create_user(request: UserInpt, db: Session):
    new_user = User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(id: int, db: Session):
    return db.query(User).filter(User.id == id).first()


def update_user(id: int, request: UserInpt, db: Session):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise ValueError(f"User with the id {id} is not available")
    user.name = request.name
    user.email = request.email
    user.password = Hash.bcrypt(request.password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def destroy_user(id: int, db: Session):
    db.query(User).filter(User.id == id).delete(synchronize_session=False)
    db.commit()
