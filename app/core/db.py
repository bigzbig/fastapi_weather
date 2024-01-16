from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings
from models.base_class import Base


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(engine)


# async def init_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all(engine))

# async def remove_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all(engine))

# async def get_db():
#     async with SessionLocal() as db:
#         try:
#             yield db
#         finally:
#             db.close()
