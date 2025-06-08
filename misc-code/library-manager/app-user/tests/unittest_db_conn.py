from contextlib import contextmanager

from sqlalchemy import create_engine, orm

from app.models.base_orm import Base

DATABASE_URL = "sqlite://"

_ENGINE = create_engine(DATABASE_URL, echo=False)
SessionLocal = orm.sessionmaker(bind=_ENGINE, autocommit=False, autoflush=False)


def _reset_schema(reset_data=True):
    orm.session.close_all_sessions()
    if reset_data:
        Base.metadata.drop_all(_ENGINE)
    Base.metadata.create_all(_ENGINE)


@contextmanager
def get_db_session(reset_data=True):
    _reset_schema(reset_data)
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()