from enum import Enum
from sqlalchemy import Column, Integer, String, CheckConstraint
from models.base_class import Base


class User(Base):
    __tablename__ = "users"

    class UserRole(Enum):
        ADMIN = "admin"
        USER = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, nullable=False)
    password = Column(String)

    role = Column(String, nullable=False, default=UserRole.USER.value)

    __table_args__ = (
        CheckConstraint(
            role in tuple([role.value for role in UserRole]),
            name="check_user_role_values",
        ),
    )
