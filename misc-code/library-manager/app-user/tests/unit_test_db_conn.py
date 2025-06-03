from contextlib import contextmanager

from sqlalchemy import create_engine, orm

from app.models.base_orm import Base

DATABASE_URL = "sqlite://"

_ENGINE = create_engine(DATABASE_URL, echo=False)
SessionLocal = orm.sessionmaker(bind=_ENGINE, autocommit=False, autoflush=False)


def _reset_schema():
    orm.session.close_all_sessions()
    Base.metadata.drop_all(_ENGINE)
    Base.metadata.create_all(_ENGINE)


@contextmanager
def get_db_session():
    _reset_schema()
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()